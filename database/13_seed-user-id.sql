UPDATE public.transactions
SET user_id = 2
WHERE user_id = 1;

UPDATE public.recurring_bills
SET user_id = 2
WHERE user_id = 1;