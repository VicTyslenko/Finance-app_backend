CREATE TABLE IF NOT EXISTS public.budgets(
    
budget_id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
user_id integer NOT NULL REFERENCES public.users(user_id) ON DELETE CASCADE,
category        text NOT NULL CHECK (category IN (
                        'Entertainment', 'Bills', 'Groceries', 'Dining Out',
                        'Transportation', 'Personal Care', 'Education',
                        'Lifestyle', 'Shopping', 'General')),
maximum_spend numeric(12,2) NOT NULL CHECK (maximum_spend > 0),
theme text NOT NULL, 
created_at timestamptz NOT NULL DEFAULT now(),
UNIQUE (user_id, category)
)