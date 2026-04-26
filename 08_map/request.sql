-- Active: 1774184466953@@127.0.0.1@3306
docker exec -i postgres psql -U metabase -d metabaseappdb << 'EOF'
CREATE TABLE IF NOT EXISTS public.my_bank_statement (
    transactiondate TEXT,
    type TEXT,
    category TEXT,
    amount TEXT,
    bonusValue TEXT
);

TRUNCATE TABLE public.my_bank_statement;

INSERT INTO public.my_bank_statement (transactiondate, type, category, amount, bonusValue)
SELECT 
    TO_CHAR(date_series, 'DD.MM.YYYY'),
    CASE WHEN random() > 0.8 THEN 'Пополнение' ELSE 'Списание' END,
    CASE 
        WHEN random() > 0.9 THEN 'Зарплата'
        WHEN random() > 0.7 THEN 'Супермаркеты'
        WHEN random() > 0.5 THEN 'Рестораны'
        WHEN random() > 0.3 THEN 'Транспорт'
        ELSE 'Развлечения'
    END,
    (random() * 5000 + 100)::numeric(10,2)::text,
    CASE WHEN random() > 0.5 THEN '+' || (random() * 100)::numeric(10,2)::text ELSE '0' END
FROM generate_series('2023-01-01'::date, '2023-12-31'::date, '1 day'::interval) AS date_series;
EOF
