# Sales Pipeline CI Testing — Design

## Intent

CI validation to test the MotherDuck gate ladder end-to-end with new dbt model changes.

## Source Mapping

| Source Table | Staging Model | Mart Model | Build Status |
|---|---|---|---|
| `salescloud.opportunity` | `stg_salescloud__opportunity` | `fct_pipeline`, `fct_pipeline_won_by_rep` | modified / new |
| `salescloud.account` | `stg_salescloud__account` | `dim_account` | existing |
| `salescloud.user` | `stg_salescloud__user` | `dim_user` | existing |

## Model Architecture

```
Sources (salescloud schema)
    ↓
Staging Layer (views)
    stg_salescloud__opportunity  ← modified (fiscal_half added)
    stg_salescloud__account
    stg_salescloud__user
    ↓
Mart Layer (tables)
    dim_account ← stg_salescloud__account
    dim_user ← stg_salescloud__user
    fct_pipeline ← stg_salescloud__opportunity + dim_account + dim_user
    fct_pipeline_won_by_rep ← fct_pipeline  ← NEW
```

## Changes in This Intent

### `stg_salescloud__opportunity` (modified)

- Added `fiscal_half` derived column: `'H1'` for Jan–Jun, `'H2'` for Jul–Dec based on close date month

### `fct_pipeline_won_by_rep` (new table)

- **Grain:** One row per sales rep (`owner_id`) per fiscal year + fiscal quarter
- **Materialization:** `table` (in `mrt` schema)
- **PK:** `rep_period_id` surrogate key (hash of `owner_id + fiscal_year + fiscal_quarter`)
- **Metrics:** `won_opportunities_count`, `total_won_amount`, `total_weighted_amount`, `avg/min/max_sales_cycle_days`
- **Source:** Reads from `fct_pipeline` (filtering `is_won = true`)

## Materialization Strategy

| Model | Materialization | Rationale |
|---|---|---|
| `stg_salescloud__opportunity` | `view` | Staging convention — lightweight rename/cast layer |
| `fct_pipeline_won_by_rep` | `table` | Aggregated mart — worth materializing for query performance |
