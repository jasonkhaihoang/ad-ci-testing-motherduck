# Design: VD-2376 Cleanup E2E

Validation intent to exercise database-cleanup.yml Dive cleanup (AC-29).

## Models modified

### `stg_salescloud__opportunity` (modified)

- **Materialization:** view
- **Grain:** one row per Salesforce opportunity; is_deleted = false filter applied; is_deleted column exposed for downstream use
- **Change:** comment-only bump — no structural change

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

### `dim_opportunity_stage`

- **Materialization:** table

### `fct_opportunity_closed_won`

- **Materialization:** table

### `fct_pipeline`

- **Materialization:** table

### `fct_pipeline_monthly_product`

- **Materialization:** table

### `fct_sales_pipeline_by_stage`

- **Materialization:** table
