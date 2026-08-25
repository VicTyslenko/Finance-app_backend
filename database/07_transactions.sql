-- The ledger: every movement of money for a user.
-- Amount sign carries direction: negative = spend, positive = income.

CREATE TABLE IF NOT EXISTS public.transactions (
    transaction_id  integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id         integer NOT NULL REFERENCES public.users(user_id) ON DELETE CASCADE,
    counterparty_id integer NOT NULL REFERENCES public.counterparties(counterparty_id),
    category        text NOT NULL CHECK (category IN (
                        'Entertainment', 'Bills', 'Groceries', 'Dining Out',
                        'Transportation', 'Personal Care', 'Education',
                        'Lifestyle', 'Shopping', 'General')),
    amount          numeric(12,2) NOT NULL CHECK (amount <> 0),
    occurred_at     timestamptz NOT NULL,
    created_at      timestamptz NOT NULL DEFAULT now()
);

-- "latest 5 transactions" and the transactions page
CREATE INDEX IF NOT EXISTS ix_transactions_user_date
    ON public.transactions (user_id, occurred_at DESC);

-- budget aggregation: SUM by category for a user
CREATE INDEX IF NOT EXISTS ix_transactions_user_category
    ON public.transactions (user_id, category);

-- Superseded by public.transactions: no dates, no counterparty, no category,
-- and unreferenced by any code or foreign key.
DROP TABLE IF EXISTS public.prices;
