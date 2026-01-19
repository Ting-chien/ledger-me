DO $$
DECLARE
    start_dt DATE;
    end_dt DATE;
    partition_name TEXT;
BEGIN
    FOR i IN 1..12 LOOP
        start_dt := TO_DATE('2026-' || i || '-01', 'YYYY-MM-DD');
        end_dt := start_dt + INTERVAL '1 month';
        partition_name := 'transactions_2026_' || LPAD(i::text, 2, '0');

        EXECUTE format(
            'CREATE TABLE IF NOT EXISTS %I PARTITION OF transactions_p 
             FOR VALUES FROM (%L) TO (%L)',
            partition_name, start_dt, end_dt
        );
    END LOOP;
END $$;