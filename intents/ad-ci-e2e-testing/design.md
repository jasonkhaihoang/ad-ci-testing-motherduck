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
