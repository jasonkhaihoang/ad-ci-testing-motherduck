# Intent: ad-ci-e2e-testing

## Summary

Add a new closed-won revenue fact model and bump the opportunity staging model to validate the e2e-and-PR-comments CI gate ladder.

## Models modified

### `stg_salescloud__opportunity` (modified)

- **Materialization:** view
- **Grain:** one row per Salesforce opportunity (excluding soft-deleted records)
- **Change:** comment-only validation bump — no structural change to columns, grain, or materialization

### `fct_opportunity_closed_won` (new)

- **Materialization:** table
- **Grain:** one row per closed-won opportunity
- **Columns:** opportunity_id (PK), account_id, owner_id, opportunity_name, stage_name, opportunity_type, lead_source, amount, probability, expected_revenue, weighted_amount, created_date, close_date, fiscal_quarter, fiscal_year, sales_cycle_days, account_name, account_type, industry, billing_country, owner_name, owner_email
- **Upstream refs:** stg_salescloud__opportunity, dim_account, dim_user
- **Purpose:** Revenue reporting, quota attainment, win-rate analysis for closed-won deals

## Downstream dependants (unmodified, included in state:modified+ closure)

The following models are downstream of `stg_salescloud__opportunity` and appear in the `state:modified+` closure. They are **not structurally changed** by this intent — included only because their upstream staging model was bumped.

### `fct_pipeline` (unmodified downstream)

- **Materialization:** table
- **Grain:** one row per opportunity (current state snapshot)
- **No structural change** — columns, grain, materialization, and unique_key unchanged

### `fct_pipeline_monthly_product` (unmodified downstream)

- **Materialization:** table
- **Grain:** one row per opportunity line item per month
- **No structural change** — columns, grain, materialization, and unique_key unchanged

### `fct_sales_pipeline_by_stage` (unmodified downstream)

- **Materialization:** table
- **Grain:** one row per opportunity per stage transition
- **No structural change** — columns, grain, materialization, and unique_key unchanged
