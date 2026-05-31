# Sales Pipeline CI Testing — Design Contract

## Intent

CI validation: add `fiscal_half` to `stg_salescloud__opportunity` and introduce `fct_pipeline_won_by_rep` mart.

## Models in state:modified+

All five models below are in the `state:modified+` closure for this PR.

---

### stg_salescloud__opportunity (modified — view)

**Grain:** One row per Salesforce opportunity (1:1 with source `salescloud.opportunity`)
**Materialization:** `view`
**Schema:** `stg`

Changes: added `fiscal_half` column (H1 for Jan–Jun, H2 for Jul–Dec, derived from close_date month).

Columns: `opportunity_id`, `account_id`, `owner_id`, `opportunity_name`, `stage_name`,
`opportunity_type`, `lead_source`, `amount`, `probability`, `expected_revenue`,
`created_date`, `close_date`, `last_stage_change_date`, `is_closed`, `is_won`,
`is_deleted`, `last_modified_date`, `system_modified_timestamp`,
`fiscal_quarter`, `fiscal_year`, `fiscal_half` (new).

---

### fct_pipeline (downstream descendant — table)

**Grain:** One row per opportunity (current snapshot, not historical)
**Materialization:** `table`
**Schema:** `mrt`

No logic changes in this PR. Downstream dependency of `stg_salescloud__opportunity`.

Columns: `opportunity_id`, `account_id`, `owner_id`, `opportunity_name`, `stage_name`,
`opportunity_type`, `lead_source`, `amount`, `probability`, `expected_revenue`,
`weighted_amount`, `created_date`, `close_date`, `last_stage_change_date`,
`is_closed`, `is_won`, `forecast_category`, `sales_cycle_days`, `opportunity_age_days`,
`days_in_current_stage`, `is_orphaned_opportunity`, `is_zero_value`,
`last_modified_date`, `system_modified_timestamp`,
`account_name`, `account_type`, `industry`, `billing_city`, `billing_state`,
`billing_country`, `owner_name`, `owner_email`, `owner_is_active`.

---

### fct_pipeline_monthly_product (downstream descendant — table)

**Grain:** One row per calendar month + product combination
**Materialization:** `table`
**Schema:** `mrt`

No logic changes in this PR. Downstream via `stg_salescloud__opportunity` join.

Columns: `close_month`, `product_id`, `product_code`, `product_name`,
`total_revenue`, `won_revenue` (and additional aggregate columns).

---

### fct_sales_pipeline_by_stage (downstream descendant — table)

**Grain:** One row per (stage_name, fiscal_year, fiscal_quarter)
**Materialization:** `table`
**Schema:** `mrt`

No logic changes in this PR. Downstream of `stg_salescloud__opportunity`.

Columns: `stage_name`, `fiscal_year`, `fiscal_quarter`, `opportunity_count`,
`won_count`, `lost_count`, `total_amount`, `weighted_amount`, `avg_probability`.

---

### fct_pipeline_won_by_rep (new — table)

**Grain:** One row per sales rep per fiscal quarter per fiscal year
**Materialization:** `table`
**Schema:** `mrt`

New model. Filters `fct_pipeline` where `is_won = true`, aggregates by rep and period.
Surrogate grain identifier: `rep_period_id` (md5 of owner_id + fiscal_year + fiscal_quarter).

Columns: `owner_id`, `owner_name`, `owner_email`, `owner_is_active`,
`fiscal_quarter`, `fiscal_year`, `rep_period_id`,
`won_opportunities_count`, `total_won_amount`, `total_weighted_amount`,
`avg_sales_cycle_days`, `min_sales_cycle_days`, `max_sales_cycle_days`,
`first_close_date`, `last_close_date`.
