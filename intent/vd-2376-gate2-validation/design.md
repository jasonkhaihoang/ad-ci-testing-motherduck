# Design: VD-2376 Gate-2 Validation

Validation intent for VD-2376 — MotherDuck Dive cleanup alongside database on PR close.

## Models modified

### `stg_salescloud__opportunity` (modified)

- **Materialization:** view
- **Grain:** one row per Salesforce opportunity (excluding soft-deleted records)
- **Change:** comment-only validation bump — no structural change

### `dim_opportunity_stage` (new)

- **Materialization:** table
- **Grain:** one row per distinct opportunity stage_name
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
