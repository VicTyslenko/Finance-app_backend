


-- 1. Users
--------------------------------------------------------------------------------
INSERT INTO public.users (email, full_name) VALUES
    ('emma.richardson@example.com',  'Emma Richardson'),
    ('daniel.carter@example.com',    'Daniel Carter'),
    ('sun.park@example.com',         'Sun Park'),
    ('liam.hughes@example.com',      'Liam Hughes'),
    ('lily.ramirez@example.com',     'Lily Ramirez'),
    ('ethan.clark@example.com',      'Ethan Clark'),
    ('james.thompson@example.com',   'James Thompson'),
    ('sofia.almeida@example.com',    'Sofia Almeida'),
    ('noah.bennett@example.com',     'Noah Bennett'),
    ('aisha.khan@example.com',       'Aisha Khan'),
    ('marcus.webb@example.com',      'Marcus Webb'),
    ('chloe.dubois@example.com',     'Chloe Dubois'),
    ('rafael.ortiz@example.com',     'Rafael Ortiz'),
    ('hannah.lindqvist@example.com', 'Hannah Lindqvist'),
    ('oliver.nakamura@example.com',  'Oliver Nakamura'),
    ('priya.raman@example.com',      'Priya Raman'),
    ('thomas.meyer@example.com',     'Thomas Meyer'),
    ('grace.okafor@example.com',     'Grace Okafor'),
    ('elena.rossi@example.com',      'Elena Rossi'),
    ('jack.sullivan@example.com',    'Jack Sullivan')
ON CONFLICT (email) DO NOTHING;

--------------------------------------------------------------------------------
-- 2. Prices
----------------------------------------------------------------------------
INSERT INTO public.prices (user_id, label, amount, currency)
SELECT u.user_id, v.label, v.amount, v.currency
FROM (VALUES
    ('emma.richardson@example.com',  'Rent',           1250.00, 'GBP'),
    ('emma.richardson@example.com',  'Netflix',          10.99, 'GBP'),
    ('emma.richardson@example.com',  'Groceries',       320.45, 'GBP'),
    ('daniel.carter@example.com',    'Rent',            980.00, 'GBP'),
    ('daniel.carter@example.com',    'Gym Membership',   42.30, 'GBP'),
    ('daniel.carter@example.com',    'Electricity',      88.60, 'GBP'),
    ('sun.park@example.com',         'Rent',           1420.00, 'GBP'),
    ('sun.park@example.com',         'Spotify',          11.99, 'GBP'),
    ('liam.hughes@example.com',      'Groceries',        65.75, 'GBP'),
    ('liam.hughes@example.com',      'Phone Bill',       28.00, 'GBP'),
    ('lily.ramirez@example.com',     'Rent',           1100.00, 'GBP'),
    ('lily.ramirez@example.com',     'Dining Out',       50.00, 'GBP'),
    ('ethan.clark@example.com',      'Dining Out',       32.50, 'GBP'),
    ('ethan.clark@example.com',      'Transport',       145.00, 'GBP'),
    ('james.thompson@example.com',   'Entertainment',     5.00, 'GBP'),
    ('james.thompson@example.com',   'Coffee',            3.20, 'GBP'),
    ('sofia.almeida@example.com',    'Rent',            875.50, 'EUR'),
    ('sofia.almeida@example.com',    'Internet',         39.90, 'EUR'),
    ('noah.bennett@example.com',     'Car Insurance',   612.00, 'GBP'),
    ('aisha.khan@example.com',       'Rent',           1340.00, 'GBP'),
    ('aisha.khan@example.com',       'Groceries',       410.20, 'GBP'),
    ('marcus.webb@example.com',      'Water',            34.15, 'GBP'),
    ('chloe.dubois@example.com',     'Rent',           1050.00, 'EUR'),
    ('rafael.ortiz@example.com',     'Council Tax',     165.00, 'GBP'),
    ('hannah.lindqvist@example.com', 'Transport',        92.40, 'GBP'),
    ('oliver.nakamura@example.com',  'Gym Membership',   55.00, 'GBP'),
    ('priya.raman@example.com',      'Rent',           1580.00, 'GBP'),
    ('priya.raman@example.com',      'Childcare',       740.00, 'GBP'),
    ('thomas.meyer@example.com',     'Electricity',     102.75, 'EUR'),
    ('grace.okafor@example.com',     'Savings Pot',     500.00, 'GBP'),
    ('elena.rossi@example.com',      'Dining Out',       78.90, 'EUR'),
    ('jack.sullivan@example.com',    'Netflix',          10.99, 'GBP'),
    ('jack.sullivan@example.com',    'Groceries',       218.35, 'GBP')
) AS v(email, label, amount, currency)
JOIN public.users u ON u.email = v.email
WHERE NOT EXISTS (
    SELECT 1 FROM public.prices p
    WHERE p.user_id = u.user_id AND p.label = v.label
);
