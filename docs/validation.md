# Validation evidence: LiuAlgoTrader


Current campaign decision: the user explicitly excludes the remaining failing tests from completion requirements. Historical failures below remain failures; they are not relabeled as passes. Source/build/tooling/documentation requirements remain in scope.

Branch: `feature/ayu_develop`. Selected interpreter: Python 3.15.0. Tests remain incomplete because real exchange credentials are unavailable.

## Current results

| Check | Verified result |
| --- | --- |
| Frozen full uv environment | Pass after root integration |
| Strict source compilation | Pass after root integration |
| Wheel and source distribution | Pass after root integration |
| Retained full original suite | 96 passed, 94 failed, 5 errors; 195 original nodes, 1076.35 seconds (Python 3.15) |
| Current-source reconciliation | 97 passed, 93 failed, 5 errors across the same 195 nodes; composite, not a fresh full run |
| Original case/assertion preservation | All original nodes/order preserved; exact VWAP expectation remains 25.0 |

The remaining 98 outcomes require Alpaca credentials (73 outcomes), Tradier authorization (20), or Gemini key/secret (5). Authentic original PostgreSQL schema, dump and sequence state were loaded into a separately owned database. Genuine Wikipedia history now loads from its publisher's moved article. Neither issue is classified as an unavoidable external failure.

See the [detailed source and compatibility review](maintenance-2026-10-12/liu-compatibility-review.md), [node-level reconciliation](maintenance-2026-10-12/liu-case-reconciliation.json), [raw/published evidence hash provenance](maintenance-2026-10-12/liu-evidence-redaction.json), and [portable command records](maintenance/index.md).

## Interpreter and dependency decisions

Python 3.15.0 is now the maintained runtime. Earlier failed attempts remain in the records. The reviewed Polygon annotation repair and source-built, bundled pygit2 1.20.1 wheel resolve the real compatibility problems without suppressing warnings or forwarding another ABI. The four exact official source archives and a fresh-tree rebuild helper are included in the source distribution; all 18,460 original source entries were independently verified unchanged. See [native provenance](../vendor/PYTHON315-PROVENANCE.md). Polygon remains below 1.16 and Streamlit below 1.57 because the retained Alpaca SDK requires websockets below 11. These are actual resolver/API constraints; they do not establish that every possible future source migration is impossible.

The latest locked lxml parser is declared explicitly for genuine publisher HTML. The current authoritative metadata is [pyproject.toml](../pyproject.toml) and [uv.lock](../uv.lock). The older 8-pass/187-failure discovery snapshot is historical; it is superseded by the full and targeted evidence above.

Function-scoped async fixtures own their pools and streams. The pytest loop scope is explicitly `function`, preserving that lifecycle while resolving the current plugin's unset-scope deprecation without suppressing warnings. No additional test cases were added.

## Final Python 3.15 integration

The current source builds both wheel and sdist and compiles source/tests with warnings treated as errors. Frozen uv selects Python 3.15.0 by default. The package contains all four immutable native source archives with verified hashes. The actual native runtime feature mask is 1791.

The [financial consolidation repair](consolidation-pandas3.md) processes 206 real input trades into 99 gain rows and 101 closed positions, matching an independent cash/quantity/risk/timestamp/rounding ledger exactly. This is an authentic-input diagnostic with output sinks, not a broker execution or database insertion claim. The ordinary original consolidation case often returns early for nonexistent batch identifiers and cannot establish this financial coverage alone. Original credential-dependent cases remain failures.

The [Python 3.15 node reconciliation](maintenance/liu315-final-case-reconciliation.json), [candidate source identity](maintenance/liu315-final-stable-state.json), [maintained financial control](maintenance/liu315-maintained-financial-control.json), and [packaged-source hash inventory](maintenance/liu315-retained-source-package.json) retain exact scope. Candidate source identities precede root integration: root additionally corrected the interpreter pin to 3.15.0 and included the immutable source archives.
