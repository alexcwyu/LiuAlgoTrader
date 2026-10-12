# LiuAlgoTrader original-case compatibility review — 2026-10-12

The reviewed isolated branch repairs reproducible local compatibility defects while preserving all 195 original case IDs, order, dates, numeric expectations, and assertion logic. The authoritative full run remains **92 passed, 98 failed, 5 errors**. Current-source targeted proofs reconcile those same nodes to **97 passed, 93 failed, 5 errors**: 98 outcomes still require authentic exchange credentials. This is a composite reconciliation, **not a fresh full-suite result** and not an all-green claim.

Implementation base: `d7442026f547ae3f776da7b931bf2d79763b9ca3`; first repair commit: `30b8c236`. Worktree: `.runtime/maintenance-2026-10-12/liu-repairs-review`, branch `feature/ayu_liu_repairs`. The root agent reviewed the production and fixture diffs and fast-forwarded the main `feature/ayu_develop` checkout to `eeaf26c2`. Main frozen uv sync, wheel/sdist build and strict source compilation subsequently passed; other repositories and unrelated containers were not modified.

## Failure evidence and resulting behavior

| Original defect | Production repair | Existing proof |
| --- | --- | --- |
| Gemini `date_range` received floating `periods` in 25 cases | Round interval count upward and use an integer boundary count; replace removed minute alias `T` with `min` | All 25 original public-provider cases passed in the full run; actual retained two-day bounds yield 58 intervals, maximum 49.655 minutes under the 50-minute budget |
| Automatic worker calculation returned zero under host load | Preserve explicit override; automatic result has minimum one | Original 20-iteration CPU-load case passed |
| Alpaca SDK was given `URL(None)` | Omit optional `base_url` when unset, retaining SDK defaults | Original constructor cases now reach authentic missing-key errors |
| Pandas removed `get_loc(method=...)` | Use `get_indexer`, reject `-1` with `KeyError`; preserve exact/ffill/nearest locations | Actual original PostgreSQL `stock_ohlc` rows execute original method ASTs: four TypeErrors before, four positions equal 3 after, missing match raises `KeyError` |
| Strategy exception handler converted the original cause into `SystemExit(0)` | Re-raise after recording traceback | Existing strategy case reaches its actual underlying missing-key cause |
| Unrequested legacy `event_loop` setup left globals/pools undefined | Await autouse resource fixtures in the running test loop; close owned pools/streams even on failed broker setup | Original DB/account/keystore/strategy/consolidation cases execute against original schema and dump |
| Warning-as-error failures from test returns, UTC construction, invalid escape | Preserve evaluated constructor/bool expressions then return `None`; use aware UTC instants and equivalent raw print string | Current-source targeted cases and strict compile succeed |
| Historical table parser dependency was undeclared | Declare and lock current `lxml` | Real Wikipedia HTML parses with lxml 6.1.3 |

Source: [Gemini](../../src/liualgotrader/data/gemini.py), [workers](../../src/liualgotrader/common/concurrency.py), [Alpaca data](../../src/liualgotrader/data/alpaca.py), [Alpaca broker](../../src/liualgotrader/trading/alpaca.py), [indexing](../../src/liualgotrader/common/data_loader.py), [support/resistance](../../src/liualgotrader/fincalcs/support_resistance.py), [strategy exception](../../src/liualgotrader/strategies/base.py), [database logging](../../src/liualgotrader/common/database.py).

## Wikipedia transport and moved historical continuation

The original implicit `read_html(URL)` request failed with HTTP 403. A transparent project User-Agent and bounded `requests.get` succeeds against the **same** [Wikipedia company article](https://en.wikipedia.org/wiki/List_of_S%26P_500_companies); official [MediaWiki REST HTML](https://www.mediawiki.org/wiki/API:REST_API/Reference/Sample_code:Get_HTML) also returned 200. Both real responses parsed to identical tables: 503 current rows and an 11-row navigation table. The second table is no longer the historical-change table.

The actual company article explicitly links [Historical components of the S&P 500](https://en.wikipedia.org/wiki/Historical_components_of_the_S%26P_500). The same-publisher linked article returns the actual 412-row Added/Removed history, with `Effective Date`, `Added/Ticker`, and `Removed/Ticker` columns and dates 1976-07-01 through 2026-10-06. The source follows this real link only when the original article lacks the semantic history columns and rejects links outside its original HTTPS publisher. No alternative vendor, cached invented roster, browser impersonation, or placeholder ticker data is used.

The original `2019-01-11` case has 164 published later changes. Repeating the complete rewind table never converges on these real add/remove cycles: three diagnostic iterations all report a change and 506 members. The repair visits every later event **once, latest first**, removes its added ticker, restores its removed ticker, then applies the unchanged original ticker-rename input in reverse date order. The diagnostic 506 count is not a new expected value or golden. Current 503 membership is not returned as a 2019 roster.

**Coverage limit:** Wikipedia presents selected changes. Date-span coverage does not independently prove a complete historical membership ledger. This repair restores the original publisher-based reconstruction intent and logs the real scope; it does not certify complete 2019 membership. The existing historical test has no complete-roster assertion. Its pass demonstrates execution of the unchanged original case, not a new claim about membership completeness.

[Source reconstruction](../../src/liualgotrader/common/market_data.py) · [actual response/transport metadata](liu-wikipedia-official-transport.json) · [moved article provenance](liu-wikipedia-moved-history.json) · [table identity](liu-wikipedia-table-contract.json) · [finite rewind diagnostic](liu-wikipedia-history-rewind-control.json). Exact attributed publisher response bodies are retained beside these records with their SHA-256 values.

| Five unchanged original Wikipedia-dependent cases | Current result |
| --- | --- |
| `tests/test_market_data.py::test_sp500_historical_constituents` | PASS |
| `tests/test_market_data.py::test_load_basic_sp500` | PASS |
| `tests/test_market_data.py::test_load_sp500_data_w_adjustments` (2019-01-11) | PASS |
| `tests/test_market_data.py::test_load_sp500_data` | FAIL: Alpaca key missing after successful real roster fetch |
| `tests/test_market_data.py::test_load_sp500_data_minute` | FAIL: Alpaca key missing after successful real roster fetch |

## Authentic PostgreSQL fixture ownership

The separate owned PostgreSQL 18.6 container `liu-maintenance-postgres-d744` listens only on `127.0.0.1:15432` with volume `liu-maintenance-postgres-d744-data`. Other containers remain untouched. The original `database/schema.sql` was applied with error-stop, then the original dump's actual COPY rows and all six original sequence `setval` statements. No market data was fabricated. Loaded row counts: 12 `algo_run`, 206 `new_trades`, 66,869 `stock_ohlc`, 7,312 `ticker_data`, zero original `trades` and `trending` rows.

Original schema SHA-256: `ae7b723a5553557172a31871ab2731d1087b6135bfe8b510a63923136922d3af`. Original dump SHA-256: `ccffa2a898d8522c578639d1a633c6625dd115d40ab62da00bc723f3375da28c`. The initial missing sequence restoration was corrected from the genuine original dump, not by altering expected test results.

All owned test processes are terminal. The owned DB password was rotated; connection with the new private DSN succeeded and the old password was rejected. The mode-0600 DSN and mode-0700 raw-evidence directory remain private under `.runtime/maintenance-2026-10-12/`. The owned container is retained for parent independent verification; it has not been represented as removed. [Owned-resource record](liu-owned-postgres.json), [original inputs](liu-original-postgres-inputs.json), [actual row index control](liu-original-db-index-control.py), [before](liu-db-index-control-before.json), [after](liu-db-index-control-after.json).

## Validation and remaining credentials

| Evidence | Result and scope |
| --- | --- |
| Original inherited discovery log | 195 nodes: 8 pass / 187 fail; exact failure taxonomy separates local setup/API defects from auth/database failures |
| Authoritative full isolated run | **92 pass / 98 fail / 5 error**, 1130.12 seconds; retained unchanged |
| Current-source targeted original cases | 16 pass / 7 missing-Alpaca failures; includes all four constructor/bool factory cases |
| Current-source five Wikipedia cases | 3 pass / 2 missing-Alpaca failures, 1.96 seconds |
| Reconciliation of identical 195 original nodes | **97 pass / 93 fail / 5 error**, composite only |
| Current strict compile | `python -Werror -m compileall -f -q src tests`: exit 0 |
| Current wheel and sdist | `uv build --python .venv/bin/python`: exit 0 |
| Edited source/test/config/report whitespace validation | `git diff --check d7442026 HEAD` scoped to these edited files: exit 0 |

The remaining 98 outcomes are **73 Alpaca missing-credential outcomes (68 failures and five setup errors), 20 real Tradier HTTP 401 failures, and five Gemini missing-key/secret assertions**. The original PostgreSQL refusal and Wikipedia 403 are not included as unavoidable external blockers. No real exchange credentials were invented or requested offline. Exact node-level results are in [case reconciliation](liu-case-reconciliation.json), with the initial snapshot and supplemental flags preserved per node.

The full run preceded two factory return corrections and the Wikipedia repair; their original cases were rerun on current source. The unchanged broad suite was not repeated. Current Pandas indexing is additionally proven with authentic original dump rows, because missing authenticated provider data prevents the original full-suite paths from reaching those indexing branches. [Full log](liu-full-existing-tests.sanitized.log), [targeted log](liu-current-source-targeted-tests.sanitized.log), [Wikipedia log](liu-wikipedia-original-tests.sanitized.log), [final build/source hashes](liu-final-build-checks.json), [original failure taxonomy](liu-original-failure-taxonomy.json), [runtime versions](liu-runtime-versions.json).

All 195 original case IDs and order are unchanged. Original assertion, raise, and condition ASTs remain unchanged except the explicitly approved positional accessor `s[-1]` to `s.iloc[-1]` in the anchored VWAP condition/message; its original exact `25.0` comparison and production Series index/type remain unchanged. Existing tests gained awaited resource ownership and current-library syntax, not additional cases, weakened assertions, skips, or changed expected returns. [Case/AST preservation proof](liu-original-case-preservation.json), [retained assertion ASTs](liu-original-assertion-ast.json).

Authentic raw logs were never rewritten. They remain private with mode 0600; published `.sanitized.log` files are separate copies with explicit credential redaction and distinct raw/published SHA-256 fields in [redaction provenance](liu-evidence-redaction.json). Equal hashes indicate no redaction was needed for that particular log. Database logging no longer prints full DSNs.

Whole-range whitespace checking flags trailing whitespace in exact publisher HTML responses and authentic pytest/psql terminal evidence. Those response/log bytes are intentionally preserved, with recorded hashes; they were not reformatted to manufacture a clean artifact check. Source, tests, config, edited Markdown/JSON, and the generated review HTML pass the scoped check. The earlier pre-staging working-diff check in the build record covered tracked edits at that time.

## Root integration verification

The strict pytest launch initially exposed an unset `asyncio_default_fixture_loop_scope` configuration. It is now explicitly `function`, matching the existing function-scoped async resource fixtures and their owned event-loop lifecycle. No warning is suppressed. The failed launch remains recorded alongside the corrected check in the [portable verification record](../maintenance/index.md).

Root strict original local cohort: **14 passed in 3.14 seconds** (`test_assets`, `test_hyperparameters`, `test_fincalc_vwap`, `test_trends`, `test_support_resistance`). Root post-integration wheel/sdist build and strict source compilation both returned exit zero. These are supplemental proofs, not a replacement full-suite result.
