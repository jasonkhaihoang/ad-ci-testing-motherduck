# Design: VD-2376 Gate-2 Validation

Validation intent for VD-2376 — MotherDuck Dive cleanup alongside database on PR close.

## Models modified

### `stg_salescloud__opportunity` (modified)

- **Materialization:** view
- **Grain:** one row per Salesforce opportunity; is_deleted = false filter applied; is_deleted column exposed for downstream use
- **Change:** comment-only validation bump — no structural change

### `dim_opportunity_stage` (new)

- **Materialization:** table
- **Grain:** one row per opportunity stage, aggregating counts and amounts across all opportunities in that stage
- **Columns:** stage_name, opportunity_count, open_count, won_count, lost_count, total_amount, open_amount, won_amount, avg_probability
- **Upstream refs:** stg_salescloud__opportunity

## Downstream models (no structural change — included in state:modified+ closure)

### `stg_salescloud__account`

- **Materialization:** view

### `stg_salescloud__user`

- **Materialization:** view

### `stg_salescloud__opportunitylineitem`

- **Materialization:** view

### `dim_account`

- **Materialization:** table

### `dim_user`

- **Materialization:** table

### `fct_opportunity_closed_won`

- **Materialization:** table

### `fct_pipeline`

- **Materialization:** table

### `fct_pipeline_monthly_product`

- **Materialization:** table

### `fct_sales_pipeline_by_stage`

- **Materialization:** table
