Review this PostgreSQL migration before it runs in production. Context: `customers` has ~4 million rows; the app currently reads and writes `customers.full_name`. The goal is to split it into `first_name` and `last_name`. The application deploy that switches reads/writes to the new columns ships right after this migration.

```sql
-- 2026_10_15_split_customer_name.sql
BEGIN;

ALTER TABLE customers ADD COLUMN first_name text;
ALTER TABLE customers ADD COLUMN last_name text;

UPDATE customers
SET first_name = split_part(full_name, ' ', 1),
    last_name  = split_part(full_name, ' ', 2);

ALTER TABLE customers ALTER COLUMN first_name SET NOT NULL;

ALTER TABLE customers DROP COLUMN full_name;

COMMIT;
```
