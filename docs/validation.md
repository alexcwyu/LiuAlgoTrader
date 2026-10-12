# Validation evidence: LiuAlgoTrader

Branch: `feature/ayu_develop`. Selected interpreter: Python 3.13.16. Tests remain incomplete because real exchange credentials are unavailable.

## Current results

| Check | Verified result |
| --- | --- |
| Frozen full uv environment | Pass after root integration |
| Strict source compilation | Pass after root integration |
| Wheel and source distribution | Pass after root integration |
| Retained full original suite | 92 passed, 98 failed, 5 errors; 195 original nodes, 1130.12 seconds |
| Current-source reconciliation | 97 passed, 93 failed, 5 errors across the same 195 nodes; composite, not a fresh full run |
| Original case/assertion preservation | All original nodes/order preserved; exact VWAP expectation remains 25.0 |

The remaining 98 outcomes require Alpaca credentials (73 outcomes), Tradier authorization (20), or Gemini key/secret (5). Authentic original PostgreSQL schema, dump and sequence state were loaded into a separately owned database. Genuine Wikipedia history now loads from its publisher's moved article. Neither issue is classified as an unavoidable external failure.

See the [detailed source and compatibility review](maintenance-2026-10-12/liu-compatibility-review.md), [node-level reconciliation](maintenance-2026-10-12/liu-case-reconciliation.json), [raw/published evidence hash provenance](maintenance-2026-10-12/liu-evidence-redaction.json), and [portable command records](maintenance/index.md).

## Interpreter and dependency decisions

Python 3.15 was attempted in an isolated environment; the failed command remains in the portable records. Python 3.14 installs the dependency graph but the retained Polygon 1.15.4 dataclass decorator assumes already-materialized annotations, which is incompatible with its lazy annotation behavior. Python 3.13.16 is the currently validated interpreter. Polygon remains below 1.16 and Streamlit below 1.57 because the retained Alpaca SDK requires websockets below 11. These are actual resolver/API constraints; they do not establish that every possible future source migration is impossible.

The latest locked lxml parser is declared explicitly for genuine publisher HTML. The current authoritative metadata is [pyproject.toml](../pyproject.toml) and [uv.lock](../uv.lock). The older 8-pass/187-failure discovery snapshot is historical; it is superseded by the full and targeted evidence above.

Function-scoped async fixtures own their pools and streams. The pytest loop scope is explicitly `function`, preserving that lifecycle while resolving the current plugin's unset-scope deprecation without suppressing warnings. No additional test cases were added.
