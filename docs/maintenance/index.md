# LiuAlgoTrader: portable verification records

These records retain exact commands, outcomes, original-log hashes and available source snapshots. Failed, interrupted and earlier exploratory commands remain visible. A later focused pass proves only its own scope.

[Machine-readable records](verification.json) · [Validation](../validation.md) · [Engineering guide](../ayu-develop.md)

Original logs remain in the workspace maintenance evidence. Tracked source hashes exclude untracked additions and later edits, as stated in each captured snapshot.

| Check | Exit | Duration | Command |
| --- | ---: | ---: | --- |
| LiuAlgoTrader-build-final.log | 0 | 1.46s | `uv build --python 3.13` |
| LiuAlgoTrader-build.log | 0 | 2.67s | `uv build --python 3.14` |
| LiuAlgoTrader-compile-final.log | 0 | 0.13s | `uv run --no-sync python -m compileall -q src` |
| LiuAlgoTrader-compile.log | 0 | 0.24s | `/Users/alex/.local/share/uv/python/cpython-3.14-macos-aarch64-none/bin/python3.14 -m compileall -q src` |
| LiuAlgoTrader-lock-3.14.log | 0 | 0.58s | `uv lock --upgrade --python 3.14` |
| LiuAlgoTrader-lock-3.15.log | 0 | 5.49s | `uv lock --upgrade --python 3.15` |
| LiuAlgoTrader-lock-runtime-fallback.log | 0 | 0.34s | `uv lock --upgrade --python 3.13` |
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
