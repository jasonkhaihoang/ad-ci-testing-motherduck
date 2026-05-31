# Sales Pipeline CI Testing — Design Contract

## Intent

Add `fiscal_half` derived column to `stg_salescloud__opportunity` and introduce `fct_pipeline_won_by_rep` as a new mart.

## Models in state:modified+

---

### stg_salescloud__opportunity

Materialization: `view` | Schema: `stg`

Grain: one row per opportunity (1:1 with source salescloud.opportunity, filtered to isdeleted=false).

Changes: added `fiscal_half` column (H1 for close months Jan–Jun, H2 for Jul–Dec).

Columns: opportunity_id, account_id, owner_id, opportunity_name, stage_name, opportunity_type, lead_source, amount, probability, expected_revenue, created_date, close_date, last_stage_change_date, is_closed, is_won, is_deleted, last_modified_date, system_modified_timestamp, fiscal_quarter, fiscal_year, fiscal_half.

---

### fct_pipeline

Materialization: `table` | Schema: `mrt`

Grain: one row per opportunity (current state snapshot).

No logic changes in this PR. Downstream of stg_salescloud__opportunity.

Columns: opportunity_id, account_id, owner_id, opportunity_name, stage_name, opportunity_type, lead_source, amount, probability, expected_revenue, weighted_amount, created_date, close_date, last_stage_change_date, is_closed, is_won, forecast_category, sales_cycle_days, opportunity_age_days, days_in_current_stage, is_orphaned_opportunity, is_zero_value, last_modified_date, system_modified_timestamp, account_name, account_type, industry, billing_city, billing_state, billing_country, owner_name, owner_email, owner_is_active.

---

### fct_pipeline_monthly_product

Materialization: `table` | Schema: `mrt`

Grain: one row per (close_month, product_id) — one calendar month and product combination.

No logic changes in this PR. Downstream via stg_salescloud__opportunity.

Columns: close_month, product_id, product_code, product_name, total_revenue, won_revenue, lost_revenue, opportunity_count, won_opportunity_count, lost_opportunity_count, total_quantity, line_item_count, avg_deal_size, avg_unit_price, avg_discount, win_rate_pct, earliest_close_date, latest_close_date.

---

### fct_sales_pipeline_by_stage

Materialization: `table` | Schema: `mrt`

Grain: one row per (stage_name, fiscal_year, fiscal_quarter).

No logic changes in this PR. Downstream of stg_salescloud__opportunity.

Columns: stage_name, fiscal_year, fiscal_quarter, opportunity_count, won_count, lost_count, total_amount, weighted_amount, avg_probability.

---

### fct_pipeline_won_by_rep

Materialization: `table` | Schema: `mrt`

Grain: one row per (owner_id, fiscal_year, fiscal_quarter) — won opportunities aggregated by sales rep and period.

New model in this PR. Reads from fct_pipeline filtered to is_won=true.

Columns: rep_period_id, owner_id, owner_name, owner_email, owner_is_active, fiscal_quarter, fiscal_year, won_opportunities_count, total_won_amount, total_weighted_amount, avg_sales_cycle_days, min_sales_cycle_days, max_sales_cycle_days, first_close_date, last_close_date.
