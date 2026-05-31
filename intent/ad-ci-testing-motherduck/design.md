# Sales Pipeline CI Testing — Design

## Context

This PR adds `fiscal_half` to `stg_salescloud__opportunity` and introduces `fct_pipeline_won_by_rep` as a new mart aggregating closed-won opportunities by sales rep and period.

## Source Mapping

| Source Table | Staging Model | Mart Model | Build Status |
|---|---|---|---|
| `salescloud.opportunity` | `stg_salescloud__opportunity` | `fct_pipeline`, `fct_pipeline_monthly_product`, `fct_sales_pipeline_by_stage`, `fct_pipeline_won_by_rep` | modified / downstream |
| `salescloud.opportunitylineitem` | `stg_salescloud__opportunitylineitem` | `fct_pipeline_monthly_product` | existing |

## Model Architecture

```
Sources (salescloud schema)
    ↓
Staging Layer (views)
    stg_salescloud__opportunity  ← modified (fiscal_half added)
    stg_salescloud__opportunitylineitem
    ↓
Mart Layer (tables)
    fct_pipeline ← stg_salescloud__opportunity + dim_account + dim_user
    fct_pipeline_monthly_product ← stg_salescloud__opportunitylineitem + stg_salescloud__opportunity
    fct_sales_pipeline_by_stage ← stg_salescloud__opportunity
    fct_pipeline_won_by_rep ← fct_pipeline  (NEW)
```

## Materialization Strategy

| Model | Materialization | Rationale |
|---|---|---|
| `stg_salescloud__opportunity` | `view` | Lightweight rename/cast layer, staging convention |
| `fct_pipeline` | `table` | Core mart, high-frequency analytics queries |
| `fct_pipeline_monthly_product` | `table` | Monthly aggregation, moderate size |
| `fct_sales_pipeline_by_stage` | `table` | Stage-level aggregation for funnel analysis |
| `fct_pipeline_won_by_rep` | `table` | Rep-level aggregation, new in this PR |

## Changes in This PR

### stg_salescloud__opportunity (modified)
- Added `fiscal_half` column: `'H1'` for close months Jan–Jun, `'H2'` for Jul–Dec, derived from `closedate` month.

### fct_pipeline_won_by_rep (new)
- New fact table aggregating closed-won opportunities by sales rep (`owner_id`) per fiscal year and quarter.
- Surrogate key `rep_period_id` = md5 hash of `(owner_id, fiscal_year, fiscal_quarter)`.
- Source: filters `fct_pipeline` where `is_won = true`.

## Grain Specification

| Model | Grain | Validation |
|---|---|---|
| `stg_salescloud__opportunity` | One row per opportunity (1:1 with source, filtered isdeleted=false) | `unique` + `not_null` test on `opportunity_id` |
| `fct_pipeline` | One row per opportunity (current state snapshot) | `unique` + `not_null` test on `opportunity_id` |
| `fct_pipeline_monthly_product` | One row per (close_month, product_id) combination | `unique_combination_of_columns` test on (`close_month`, `product_id`) |
| `fct_sales_pipeline_by_stage` | One row per (stage_name, fiscal_year, fiscal_quarter) | No single-column unique test; grain enforced by GROUP BY |
| `fct_pipeline_won_by_rep` | One row per (owner_id, fiscal_year, fiscal_quarter) | `unique` + `not_null` on `rep_period_id`; `unique_combination_of_columns` on (`owner_id`, `fiscal_year`, `fiscal_quarter`) |

## Column Notes

### stg_salescloud__opportunity
All existing columns preserved. New column `fiscal_half` (string: H1 or H2) added after `fiscal_year`.

### fct_pipeline_won_by_rep
Key columns: `rep_period_id` (surrogate key), `owner_id`, `owner_name`, `owner_email`, `owner_is_active`, `fiscal_quarter`, `fiscal_year`, `won_opportunities_count`, `total_won_amount`, `total_weighted_amount`, `avg_sales_cycle_days`, `min_sales_cycle_days`, `max_sales_cycle_days`, `first_close_date`, `last_close_date`.
