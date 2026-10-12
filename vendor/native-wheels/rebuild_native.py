#!/usr/bin/env python3
"""Rebuild the reviewed cp315/macOS-arm64 wheel from retained official sources.

This helper creates a fresh owned build tree. It never installs libraries or
packages into a system prefix or an existing project environment.
"""
from __future__ import annotations

import argparse
import base64
import csv
import hashlib
import io
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import tarfile
import tempfile
import zipfile

SOURCES = {
    "openssl": ("liu315-openssl-official-source.tar.gz", "84af0ce70add3a4880379de17aef6ee084f1ec109b166817be3f0a6feb4e6240"),
    "libssh2": ("liu315-libssh2-official-source.tar.gz", "40eab1872718e58670cf24596810160a3e3c2372030cb085e4d2f7ec876bacb2"),
    "libgit2": ("liu315-libgit2-official-source.tar.gz", "08fe5bc4a9561da53ff700f7ce22a0f068882a037dd253c988be397419d60e5a"),
    "pygit2": ("liu315-pygit2-original.tar.gz", "36dff84d237f2b8f18b0b146d6e7c3f99a7bce2da98cc4103a14387f53319f95"),
}


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()



def verify_source_archives(work: Path, archive_root: Path) -> dict:
    checks = {}
    for name, (filename, expected) in SOURCES.items():
        archive = archive_root / filename
        assert digest(archive.read_bytes()) == expected
        entries = 0
        changed = []
        with tarfile.open(archive) as package:
            for member in package:
                path = work / "source" / name / member.name
                if member.isfile():
                    entries += 1
                    if not path.is_file() or path.read_bytes() != package.extractfile(member).read():
                        changed.append(member.name)
                elif member.issym():
                    entries += 1
                    if not path.is_symlink() or os.readlink(path) != member.linkname:
                        changed.append(member.name)
        assert not changed, (name, changed)
        checks[name] = {"original_entries_checked": entries, "changed_archive_entries": changed}
    return checks


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--python", default=sys.executable, help="Managed CPython 3.15 executable")
    parser.add_argument("--archive-root", type=Path, default=Path(__file__).resolve().parent.parent / "native-sources")
    parser.add_argument("--work-parent", type=Path, default=None, help="Optional owned build parent; defaults to the system temporary directory")
    parser.add_argument("--verify-existing-tree", type=Path, help="Verify original source entries after a retained completed rebuild")
    args = parser.parse_args()
    if args.verify_existing_tree:
        print(json.dumps(verify_source_archives(args.verify_existing_tree, args.archive_root), indent=2))
        return
    assert sys.platform == "darwin" and platform.machine() == "arm64", "This reviewed build targets macOS arm64"
    version = subprocess.check_output([args.python, "-c", "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')"], text=True).strip()
    assert version == "3.15", version
    work = Path(tempfile.mkdtemp(prefix="liu315-native-rebuild-", dir=args.work_parent)).resolve()
    logs = work / "logs"
    logs.mkdir()
    records: list[dict] = []

    def run(name: str, command: list[str], *, cwd: Path = work, env: dict | None = None) -> None:
        log = logs / f"{len(records):02d}-{name}.log"
        with log.open("xb") as output:
            result = subprocess.run(command, cwd=cwd, env=env, stdout=output, stderr=subprocess.STDOUT)
        records.append({"name": name, "command": command, "cwd": str(cwd), "exit": result.returncode, "log": str(log), "log_sha256": digest(log.read_bytes())})
        (work / "commands.json").write_text(json.dumps(records, indent=2) + "\n")
        if result.returncode:
            raise RuntimeError(f"{name} failed with exit {result.returncode}; exact log: {log}")
        print(name, "PASS", flush=True)

    source: dict[str, Path] = {}
    for name, (filename, expected) in SOURCES.items():
        archive = args.archive_root / filename
        assert digest(archive.read_bytes()) == expected, f"Original source hash differs: {archive}"
        destination = work / "source" / name
        destination.mkdir(parents=True)
        with tarfile.open(archive) as package:
            package.extractall(destination, filter="data")
        source[name] = destination / "pygit2-1.20.1" if name == "pygit2" else destination
    prefix = {name: work / "prefix" / name for name in ("openssl", "libssh2", "libgit2")}
    openssl_build = work / "build" / "openssl"
    openssl_build.mkdir(parents=True)
    run("openssl-configure", [str(source["openssl"] / "Configure"), "darwin64-arm64-cc", "shared", "no-apps", "no-docs", "no-tests", "-mmacosx-version-min=11.0", f"--prefix={prefix['openssl']}", "--libdir=lib"], cwd=openssl_build)
    run("openssl-build", ["make", "-j1"], cwd=openssl_build)
    run("openssl-install", ["make", "install"], cwd=openssl_build)
    for name, extra in (
        ("libssh2", ["-DBUILD_EXAMPLES=OFF", "-DBUILD_TESTING=OFF", f"-DOPENSSL_ROOT_DIR={prefix['openssl']}"]),
        ("libgit2", ["-DBUILD_TESTS=OFF", "-DUSE_SSH=ON", f"-DCMAKE_PREFIX_PATH={prefix['libssh2']}", f"-DCMAKE_INSTALL_RPATH={prefix['libssh2'] / 'lib'}"]),
    ):
        build = work / "build" / name
        run(name + "-configure", ["cmake", "-S", str(source[name]), "-B", str(build), f"-DCMAKE_INSTALL_PREFIX={prefix[name]}", "-DCMAKE_OSX_DEPLOYMENT_TARGET=11.0", "-DCMAKE_BUILD_TYPE=Release", *extra])
        run(name + "-build-install", ["cmake", "--build", str(build), "--target", "install", "--parallel", "1"])
    native_env = os.environ.copy()
    native_env.update({"LIBGIT2": str(prefix["libgit2"]), "MACOSX_DEPLOYMENT_TARGET": "11.0", "UV_CONCURRENT_BUILDS": "1", "LDFLAGS": " ".join(f"-Wl,-rpath,{prefix[name] / 'lib'}" for name in ("libgit2", "libssh2", "openssl"))})
    unrepaired = work / "unrepaired"
    run("pygit2-source-wheel", ["uv", "build", "--wheel", "--python", args.python, "--out-dir", str(unrepaired), str(source["pygit2"])], env=native_env)
    original_wheel = next(unrepaired.glob("*.whl"))
    repaired = work / "wheel"
    run("delocate", ["uv", "run", "--no-project", "--python", args.python, "--with", "delocate==0.13.0", "delocate-wheel", "--require-target-macos-version=11.0", "-w", str(repaired), str(original_wheel)])
    wheel = next(repaired.glob("*.whl"))
    assert wheel.name == "pygit2-1.20.1-cp315-cp315-macosx_11_0_arm64.whl", wheel.name
    with zipfile.ZipFile(wheel) as package:
        entries = {name: package.read(name) for name in package.namelist()}
    record = next(name for name in entries if name.endswith(".dist-info/RECORD"))
    license_root = record.rsplit("/", 1)[0] + "/licenses/"
    for name, filename in (("libgit2", "COPYING"), ("libssh2", "COPYING"), ("openssl", "LICENSE.txt")):
        entries[license_root + name.upper() + "-" + filename] = (source[name] / filename).read_bytes()
    buffer = io.StringIO()
    writer = csv.writer(buffer, lineterminator="\n")
    for name, data in entries.items():
        if name != record:
            writer.writerow([name, "sha256=" + base64.urlsafe_b64encode(hashlib.sha256(data).digest()).rstrip(b"=").decode(), str(len(data))])
    writer.writerow([record, "", ""])
    entries[record] = buffer.getvalue().encode()
    temporary = wheel.with_suffix(".tmp")
    with zipfile.ZipFile(temporary, "w", zipfile.ZIP_DEFLATED) as package:
        for name, data in entries.items():
            package.writestr(name, data)
    temporary.replace(wheel)
    extracted = work / "wheel-inspection"
    with zipfile.ZipFile(wheel) as package:
        package.extractall(extracted)
    libraries = {}
    for path in extracted.rglob("*"):
        if path.suffix not in (".so", ".dylib"):
            continue
        dependencies = subprocess.check_output(["otool", "-L", str(path)], text=True)
        load_commands = subprocess.check_output(["otool", "-l", str(path)], text=True)
        assert str(work) not in "\n".join(dependencies.splitlines()[1:]), dependencies
        assert str(work) not in "\n".join(line for line in load_commands.splitlines() if "path " in line), load_commands
        assert "minos 11.0" in load_commands or "version 11.0" in load_commands, load_commands
        libraries[str(path.relative_to(extracted))] = {"dependencies": dependencies.splitlines()[1:], "minimum_macos": "11.0", "sha256": digest(path.read_bytes())}
    control = work / "control-venv"
    run("create-control-venv", ["uv", "venv", "--python", args.python, str(control)])
    run("install-control-wheel", ["uv", "pip", "install", "--python", str(control / "bin/python"), str(wheel)])
    unavailable = []
    try:
        for path in prefix.values():
            hidden = path.with_name(path.name + "-unavailable-control")
            path.rename(hidden)
            unavailable.append((path, hidden))
        run("import-without-build-prefixes", [str(control / "bin/python"), "-c", "import pygit2; assert pygit2.features == 1791; assert pygit2.LIBGIT2_VERSION == '1.9.7'; print(pygit2.__version__, pygit2.LIBGIT2_VERSION, pygit2.features)"])
    finally:
        for path, hidden in reversed(unavailable):
            hidden.rename(path)
    source_checks = verify_source_archives(work, args.archive_root)
    report = {"source_after_build_checks": source_checks, "sources_sha256": {name: expected for name, (_, expected) in SOURCES.items()}, "wheel": str(wheel), "wheel_sha256": digest(wheel.read_bytes()), "library_checks": libraries, "licensed_native_components": sorted(name for name in entries if "/licenses/" in name), "features": 1791, "runtime_without_build_prefixes": True, "minimum_deployment_target": "11.0", "bit_identical_wheel_claim": False, "source_changes": [], "commands": records}
    (work / "result.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"result": str(work / "result.json"), "wheel": str(wheel), "wheel_sha256": report["wheel_sha256"]}), flush=True)


if __name__ == "__main__":
    main()
