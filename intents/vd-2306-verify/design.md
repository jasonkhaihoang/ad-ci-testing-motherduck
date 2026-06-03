# Intent: vd-2306-verify

## Summary

Comment-only bump to `fct_opportunity_closed_won` to verify the VD-2306 fix: the
`ci/data-tests` "Per model" block should attribute each test to its parent model name
(not blank) after deploying the `attached_node` fallback in `parse_run_results.py`.

## Models modified

### `fct_opportunity_closed_won` (modified)

- **Materialization:** table
- **Grain:** one row per closed-won opportunity
- **Change:** comment-only validation bump — no structural change to columns, grain, or materialization
- **Columns:** opportunity_id (PK), account_id, owner_id, opportunity_name, stage_name, opportunity_type, lead_source, amount, probability, expected_revenue, weighted_amount, created_date, close_date, fiscal_quarter, fiscal_year, sales_cycle_days, account_name, account_type, industry, billing_country, owner_name, owner_email
