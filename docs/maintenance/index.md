# LiuAlgoTrader: portable verification records

Full raw logs are retained in the workspace maintenance evidence, not distributed here. Hashes identify those original logs. A successful build or selected test subset does not imply a full test-suite pass. Commands containing <workspace> describe the original execution environment.

[Machine-readable records](verification.json) · [Repository validation summary](../validation.md)

## Executed commands

| Check | Exit | Duration | Command | Outcomes |
| --- | ---: | ---: | --- | --- |
| build | 0 | 2.67s | `uv build --python 3.14` | Successfully built dist/liualgotrader-0.4.35.tar.gz<br>Successfully built dist/liualgotrader-0.4.35-py3-none-any.whl |
| build-final | 0 | 1.46s | `uv build --python 3.13` | Successfully built dist/liualgotrader-0.4.35.tar.gz<br>Successfully built dist/liualgotrader-0.4.35-py3-none-any.whl |
| compile | 0 | 0.24s | `/Users/alex/.local/share/uv/python/cpython-3.14-macos-aarch64-none/bin/python3.14 -m compileall -q src` | See exit status; no test-count assertion. |
| compile-final | 0 | 0.13s | `uv run --no-sync python -m compileall -q src` | See exit status; no test-count assertion. |
| lock-3.14 | 0 | 0.58s | `uv lock --upgrade --python 3.14` | See exit status; no test-count assertion. |
| lock-3.15 | 0 | 5.49s | `uv lock --upgrade --python 3.15` | See exit status; no test-count assertion. |
| lock-runtime-fallback | 0 | 0.34s | `uv lock --upgrade --python 3.13` | See exit status; no test-count assertion. |
| python315-source-probe | 1 | 3.24s | `uv sync --directory /tmp/trading-python315-probes/LiuAlgoTrader --all-extras --all-groups --python 3.15` | See exit status; no test-count assertion. |
| sync-3.14 | 0 | 5.5s | `uv sync --all-extras --all-groups --python 3.14` | See exit status; no test-count assertion. |
| sync-runtime-fallback | 0 | 5.84s | `uv sync --all-extras --all-groups --python 3.13` | See exit status; no test-count assertion. |
| tests | 2 | 17.15s | `uv run --no-sync python -m pytest` | See exit status; no test-count assertion. |
| tests-default-discovery | 1 | unrecordeds | `uv run --no-sync python -m pytest` | =================== 187 failed, 8 passed in 88.32s (0:01:28) =================== |
| tests-runtime-fallback | 4 | 2.71s | `uv run --no-sync python -m pytest` | See exit status; no test-count assertion. |
| versions-final | 0 | 0.24s | `uv run --no-sync python -c import sys,importlib.metadata,json; print(sys.version); print(json.dumps({d.metadata["Name"]: d.version for d in importlib.metadata.distributions()},indent=2,sort_keys=True))` | See exit status; no test-count assertion. |
| wheel-probe-3.14 | 2 | 0.05s | `uv sync --all-extras --all-groups --python 3.14 --no-build --no-install-project` | See exit status; no test-count assertion. |
| wheel-probe-3.15 | 2 | 0.04s | `uv sync --all-extras --all-groups --python 3.15 --no-build --no-install-project` | See exit status; no test-count assertion. |
