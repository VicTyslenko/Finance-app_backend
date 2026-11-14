-- A recurring bill is the schedule ("pay Spark £100 on the 2nd every month").
-- The payments it produces live in public.transactions; a bill counts as paid
-- for the month when a matching transaction exists for that month.

CREATE TABLE IF NOT EXISTS public.recurring_bills (
    bill_id         integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id         integer NOT NULL REFERENCES public.users(user_id) ON DELETE CASCADE,
    counterparty_id integer NOT NULL REFERENCES public.counterparties(counterparty_id),
    category        text NOT NULL CHECK (category IN (
                        'Entertainment', 'Bills', 'Groceries', 'Dining Out',
                        'Transportation', 'Personal Care', 'Education',
                        'Lifestyle', 'Shopping', 'General')),
    amount          numeric(12,2) NOT NULL CHECK (amount > 0),
    due_day         smallint NOT NULL CHECK (due_day BETWEEN 1 AND 31),
    created_at      timestamptz NOT NULL DEFAULT now(),
    UNIQUE (user_id, counterparty_id)
);

-- Emma Richardson's (user_id 1) bills from the design. Total = 384.98.
-- Amounts are positive here: a bill is what you owe, the transaction is the
-- money leaving (negative) when it gets paid.
INSERT INTO public.recurring_bills (user_id, counterparty_id, category, amount, due_day)
SELECT 1, c.counterparty_id, v.category, v.amount, v.due_day
FROM (VALUES
    ('spark-electric-solutions',  'Bills',          100.00,  2),
    ('serenity-spa-and-wellness', 'Personal Care',   30.00,  3),
    ('elevate-education',         'Bills',           50.00,  4),
    ('pixel-playground',          'Entertainment',   10.00, 11),
    ('nimbus-data-storage',       'Lifestyle',        9.99, 21),
    ('bytewise',                  'Lifestyle',       49.99, 23),
    ('ecofuel-energy',            'Bills',           35.00, 29),
    ('aqua-flow-utilities',       'Bills',          100.00, 30)
) AS v(slug, category, amount, due_day)
JOIN public.counterparties c ON c.slug = v.slug
ON CONFLICT (user_id, counterparty_id) DO NOTHING;
