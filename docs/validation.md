# Validation evidence: LiuAlgoTrader

Run date: 2026-10-12. Branch: `feature/ayu_develop`. Interpreter: `3.13.16 (main, Oct  9 2026, 15:11:24) [Clang 22.1.3 ]`.

| Check | Result |
|---|---|
| lock | passed |
| sync | passed |
| compile | passed |
| build | passed |
| tests | failed |

## Current result and compatibility decisions

- Python 3.14 exposes the Polygon 1.15.4 dataclass decorator assumption that __annotations__ is already materialized; existing full suite was therefore executed with managed 3.13.16.
- Polygon is constrained below 1.16 and Streamlit below 1.57 because the retained Alpaca trade SDK requires websockets<11. These are resolver-backed compatibility constraints.
- The full existing integration suite needs a configured PostgreSQL connection pool and Alpaca, Polygon, Tradier and other venue credentials. Missing setup produces 187 failures; no cases were disabled.

Current unresolved checks:

- tests: exit 1; see [check record](maintenance/index.html)

## Latest full-suite output

```text
range4 - Value...
FAILED tests/test_alpaca_stream.py::test_crypto_stream - TypeError: Unexpecte...
FAILED tests/test_alpaca_trader.py::test_get_symbols - NameError: name 'alpac...
FAILED tests/test_alpaca_trader.py::test_get_shortable_symbols - NameError: n...
FAILED tests/test_alpaca_trader.py::test_is_fractionable - NameError: name 'a...
FAILED tests/test_alpacadata.py::test_get_trading_day - ValueError: ('Key ID ...
FAILED tests/test_analysis.py::test_returns - OSError: Multiple exceptions: [check record](maintenance/index.html) |
| `uv sync --all-extras --all-groups --python 3.15 --no-build --no-install-project` | 2 | 0.04 | [check record](maintenance/index.html) |
| `uv lock --upgrade --python 3.14` | 0 | 0.58 | [check record](maintenance/index.html) |
| `uv sync --all-extras --all-groups --python 3.14 --no-build --no-install-project` | 2 | 0.05 | [check record](maintenance/index.html) |
| `uv sync --all-extras --all-groups --python 3.14` | 0 | 5.5 | [check record](maintenance/index.html) |
| `uv build --python 3.14` | 0 | 2.67 | [check record](maintenance/index.html) |
| `/Users/alex/.local/share/uv/python/cpython-3.14-macos-aarch64-none/bin/python3.14 -m compileall -q src` | 0 | 0.24 | [check record](maintenance/index.html) |
| `uv run --no-sync python -m pytest` | 2 | 17.15 | [check record](maintenance/index.html) |
| `uv lock --upgrade --python 3.13` | 0 | 0.34 | [check record](maintenance/index.html) |
| `uv sync --all-extras --all-groups --python 3.13` | 0 | 5.84 | [check record](maintenance/index.html) |
| `uv run --no-sync python -m pytest` | 4 | 2.71 | [check record](maintenance/index.html) |
| `uv run --no-sync python -m pytest` | 1 | 90.71 | [check record](maintenance/index.html) |
| `uv run --no-sync python -m compileall -q src` | 0 | 0.13 | [check record](maintenance/index.html) |
| `uv build --python 3.13` | 0 | 1.46 | [check record](maintenance/index.html) |
| `uv run --no-sync python -c import sys,importlib.metadata,json; print(sys.version); print(json.dumps({d.metadata["Name"]: d.version for d in importlib.metadata.distributions()},indent=2,sort_keys=True))` | 0 | 0.24 | [check record](maintenance/index.html) |
| `uv sync --directory /tmp/trading-python315-probes/LiuAlgoTrader --all-extras --all-groups --python 3.15` | 1 | 3.24 | [check record](maintenance/index.html) |

The versions-final log records the exact interpreter patch release and every installed dependency version. The machine-readable [verification record](maintenance/verification.json) includes branch/default ancestry, status, artifacts and unresolved checks.

## Dependency floor refresh

| Before | After |
|---|---|

The table records the initial metadata refresh. Later compatibility constraints and vendor sources are explained above and the final authoritative requirements are in [pyproject.toml](../pyproject.toml) and [uv.lock](../uv.lock). No test cases were added, removed or disabled. Existing deprecated-API cases retain their assertions while explicitly checking the documented warning.
