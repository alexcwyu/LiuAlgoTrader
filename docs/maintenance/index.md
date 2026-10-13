# LiuAlgoTrader: portable verification records

<!-- current-documentation-provenance -->
Documentation reviewed: 2026-10-13 / Git source base: `415d67259015f0a258bb9d92a8a46daa43b17086` / [Current architecture and feature guide](../ayu-develop.md).
Historical execution commands/results below retain their original dates and scope; this metadata update is not a new application test run.
<!-- /current-documentation-provenance -->


These records retain exact commands, outcomes, original-log hashes and available source snapshots. Failed, interrupted and earlier exploratory commands remain visible. A later focused pass proves only its own scope.

[Machine-readable records](verification.json) · [Validation](../validation.md) · [Engineering guide](../ayu-develop.md)

Original logs remain in the workspace maintenance evidence. Tracked source hashes exclude untracked additions and later edits, as stated in each captured snapshot.

| Check | Exit | Duration | Command |
| --- | ---: | ---: | --- |
| LiuAlgoTrader-build-final.log | 0 | 1.46s | `uv build --python 3.13` |
| LiuAlgoTrader-build.log | 0 | 2.67s | `uv build --python 3.14` |
| LiuAlgoTrader-compile-final.log | 0 | 0.13s | `uv run --no-sync python -m compileall -q src` |
| LiuAlgoTrader-compile.log | 0 | 0.24s | `/Users/alex/.local/share/uv/python/cpython-3.14-macos-aarch64-none/bin/python3.14 -m compileall -q src` |
| authentic-financial-consolidation-control | 0 | Nones | `<workspace>/.runtime/maintenance-2026-10-12/liu315-feasibility-3544/.venv/bin/python control-evidence/run_finance_control.py` |
| LiuAlgoTrader-lock-3.14.log | 0 | 0.58s | `uv lock --upgrade --python 3.14` |
| LiuAlgoTrader-lock-3.15.log | 0 | 5.49s | `uv lock --upgrade --python 3.15` |
| LiuAlgoTrader-lock-runtime-fallback.log | 0 | 0.34s | `uv lock --upgrade --python 3.13` |
| main315-default-frozen-sync | 0 | 0.04s | `uv sync --frozen --all-groups --all-extras` |
| main315-finance-authentic-control | 0 | 2.15s | `uv run --no-sync python ../docs/maintenance-2026-10-12/tools/run_liu_finance_main.py` |
| main315-finance-build | 0 | 1.53s | `uv build` |
| main315-finance-compile | 0 | 0.13s | `uv run --no-sync python -Werror -m compileall -q -f src tests` |
| main315-finance-original-owned-db-cases | 1 | 0.88s | `uv run --no-sync python ../docs/maintenance-2026-10-12/tools/run_liu_private_finance_cases.py` |
| main315-frozen-full-sync | 0 | 1.17s | `uv sync --frozen --all-groups --all-extras --python 3.15.0` |
| main315-local-original-cases | 0 | 6.5s | `uv run --no-sync python -W error -m pytest tests/test_assets.py tests/test_hyperparameters.py tests/test_fincalc_vwap.py tests/test_trends.py tests/test_support_resistance.py -q` |
| main315-native-runtime | 0 | 0.5s | `uv run --no-sync python -W error -c import sys,json,pygit2,polygon,numpy,pandas,scipy,asyncpg; print(json.dumps({"python":sys.version,"pygit2":pygit2.__version__,"libgit2":pygit2.LIBGIT2_VERSION,"features":pygit2.features,"numpy":numpy.__version__,"pandas":pandas.__version__,"scipy":scipy.__version__})); assert sys.version_info[:2]==(3,15); assert pygit2.features==1791` |
| main315-owned-db-original-cases | 1 | 1.32s | `uv run --no-sync python ../docs/maintenance-2026-10-12/tools/run_liu_private_cases.py` |
| main315-retained-sources-build | 0 | 1.64s | `uv build` |
| main315-retained-sources-compile | 0 | 0.18s | `uv run --no-sync python -Werror -m compileall -q -f src tests vendor/native-wheels/rebuild_native.py` |
| main315-source-test-compile | 0 | 0.19s | `uv run --no-sync python -W error -m compileall -q -f src tests` |
| main315-wheel-sdist | 0 | 1.54s | `uv build` |
| LiuAlgoTrader-python315-source-probe.log | 1 | 3.24s | `uv sync --directory /tmp/trading-python315-probes/LiuAlgoTrader --all-extras --all-groups --python 3.15` |
| reviewed-local-cases-function-loop | 0 | 3.48s | `uv run --no-sync python -W error -m pytest tests/test_assets.py tests/test_hyperparameters.py tests/test_fincalc_vwap.py tests/test_trends.py tests/test_support_resistance.py -q` |
| reviewed-local-cases | 3 | 0.21s | `uv run --no-sync python -W error -m pytest tests/test_fincalc_vwap.py tests/test_support_resistance.py tests/test_data_date_ranges.py -q` |
| reviewed-source-compile | 0 | 0.14s | `uv run --no-sync python -W error -m compileall -q -f src` |
| reviewed-wheel-sdist | 0 | 0.75s | `uv build` |
| LiuAlgoTrader-sync-3.14.log | 0 | 5.5s | `uv sync --all-extras --all-groups --python 3.14` |
| LiuAlgoTrader-sync-runtime-fallback.log | 0 | 5.84s | `uv sync --all-extras --all-groups --python 3.13` |
| LiuAlgoTrader-tests-default-discovery.log | 1 | unknowns | `uv run --no-sync python -m pytest` |
| LiuAlgoTrader-tests-runtime-fallback.log | 4 | 2.71s | `uv run --no-sync python -m pytest` |
| LiuAlgoTrader-tests.log | 2 | 17.15s | `uv run --no-sync python -m pytest` |
| LiuAlgoTrader-versions-final.log | 0 | 0.24s | `uv run --no-sync python -c import sys,importlib.metadata,json; print(sys.version); print(json.dumps({d.metadata["Name"]: d.version for d in importlib.metadata.distributions()},indent=2,sort_keys=True))` |
| LiuAlgoTrader-wheel-probe-3.14.log | 2 | 0.05s | `uv sync --all-extras --all-groups --python 3.14 --no-build --no-install-project` |
| LiuAlgoTrader-wheel-probe-3.15.log | 2 | 0.04s | `uv sync --all-extras --all-groups --python 3.15 --no-build --no-install-project` |
