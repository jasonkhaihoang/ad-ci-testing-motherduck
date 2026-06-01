# VD-2293: Fix CREATE DATABASE fails on free-plan MotherDuck

## Summary

Gate 2 clone step fails on free-plan MotherDuck accounts because `CREATE DATABASE pr_N_sha FROM prd` inherits prd's 7-day snapshot retention, which the free plan rejects with "Invalid storage retention specified: 7 snapshot retention days invalid for plan free".

## Fix

Add `ALTER DATABASE pr_N_sha SET SNAPSHOT_RETENTION_DAYS = 0` immediately after the clone. This is a no-op on paid plans where 0-day retention is already the default.

## Models in scope

- `stg_salescloud__opportunity` (modified — validation bump)
- `dim_closed_won_opportunity` (new — closed-won dimension table)

## Design decisions

- `SNAPSHOT_RETENTION_DAYS 0` cannot be set in the `CREATE DATABASE … FROM` clause; only `SNAPSHOT_ID`, `SNAPSHOT_NAME`, `SNAPSHOT_TIME` are valid there. The fix must use a post-CREATE `ALTER DATABASE` call.
- Always set to 0 regardless of plan — avoids conditional logic and the ALTER is a no-op on paid plans.
