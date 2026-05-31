# Sales Pipeline CI Testing — Design

## Changes

This PR makes two changes to the sales pipeline dbt project:

1. **stg_salescloud__opportunity** (staging, view): adds a new derived column `fiscal_half`
   that classifies the opportunity's close date into H1 (January–June) or H2 (July–December).
   All existing columns are unchanged. No new sources or references.

2. **fct_pipeline_won_by_rep** (new mart, table): a new aggregated fact table that groups
   closed-won opportunities by sales rep and fiscal period. References `fct_pipeline`.

## Models in scope

| Model | Materialization | Change |
|---|---|---|
| `stg_salescloud__opportunity` | view | Modified — `fiscal_half` column added |
| `fct_pipeline` | table | Downstream rebuild, no logic changes |
| `fct_pipeline_monthly_product` | table | Downstream rebuild, no logic changes |
| `fct_sales_pipeline_by_stage` | table | Downstream rebuild, no logic changes |
| `fct_pipeline_won_by_rep` | table | New model |

## stg_salescloud__opportunity

Grain: one row per Salesforce opportunity (filtered to `isdeleted = false`).

The only change is the addition of the `fiscal_half` column.

## fct_pipeline

Grain: one row per opportunity. No changes to logic or columns in this PR.

## fct_pipeline_monthly_product

Grain: one row per (close_month, product_id). No changes to logic or columns in this PR.

## fct_sales_pipeline_by_stage

Grain: one row per (stage_name, fiscal_year, fiscal_quarter). No changes in this PR.

## fct_pipeline_won_by_rep

Grain: one row per (owner_id, fiscal_year, fiscal_quarter).
New table materialized in the `mrt` schema.
Reads from `fct_pipeline` filtered to `is_won = true`.
Aggregates metrics per rep per period: count, total revenue, weighted revenue, sales cycle stats.
Includes a surrogate identifier column `rep_period_id`.
