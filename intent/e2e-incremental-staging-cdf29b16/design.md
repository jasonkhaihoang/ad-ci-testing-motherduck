# Design: E2E incremental-staging VD-2282

## Source Mapping
| Source Table | Staging Model | Status |
|---|---|---|
| `salescloud.opportunity` | `stg_salescloud__opportunity` | **Modified** |

## Model Architecture
Modification to existing staging model for E2E incremental-staging test.

## Build Sequence
1. Run `stg_salescloud__opportunity` (staging, modified)

## Grain
- `stg_salescloud__opportunity`: one row per opportunity
