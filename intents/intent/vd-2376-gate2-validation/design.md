# Design: VD-2376 Gate-2 Validation

Validation intent for VD-2376 — MotherDuck Dive cleanup alongside database on PR close.

## Models modified

### `stg_salescloud__opportunity` (modified)

- **Materialization:** view
- **Grain:** one row per Salesforce opportunity (excluding soft-deleted records)
- **Change:** comment-only validation bump — no structural change to columns, grain, or materialization
- **Columns:** opportunity_id (PK), account_id, owner_id, opportunity_name, stage_name, opportunity_type, lead_source, amount, probability, expected_revenue, weighted_amount, created_date, close_date, last_stage_change_date, is_closed, is_won, is_deleted, last_modified_date, system_modified_timestamp, fiscal_quarter, fiscal_year

### `dim_opportunity_stage` (new)

- **Materialization:** table
- **Grain:** one row per distinct opportunity stage_name
- **Columns:** stage_name (PK), opportunity_count, open_count, won_count, lost_count, total_amount, open_amount, won_amount, avg_probability
- **Upstream refs:** stg_salescloud__opportunity
- **Purpose:** Stage-level pipeline summary for reporting on opportunity distribution by stage
