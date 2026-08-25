-- Emma Richardson's (user_id 1) ledger, sized to reproduce the design's figures:
--   Income 3,814.25 · Expenses 1,700.50 · budgeted spend 338.00
--   Entertainment 15.00 · Bills 150.00 · Dining Out 133.00 · Personal Care 40.00
--
-- Dates are relative so "this month" queries always find them. Current-month
-- rows are clamped to the month start, so the aggregates stay correct whenever
-- the seed happens to run; prev_month rows sit deliberately outside the window
-- to prove the month filtering works.

INSERT INTO public.transactions (user_id, counterparty_id, category, amount, occurred_at)
SELECT 1,
       c.counterparty_id,
       v.category,
       v.amount,
       CASE
           WHEN v.prev_month
               THEN date_trunc('month', now()) - (v.hours_ago || ' hours')::interval
           ELSE GREATEST(now() - (v.hours_ago || ' hours')::interval,
                         date_trunc('month', now()))
       END
FROM (VALUES
    -- ── this month: income ──────────────────────────────────────────────────
    ('buzz-marketing-group',      'General',        3618.75,  360, false),
    ('emma-richardson',           'General',          75.50,   48, false),
    ('sun-park',                  'General',         120.00,   96, false),

    -- ── this month: budgeted spend ──────────────────────────────────────────
    ('james-thompson',            'Entertainment',    -5.00,  240, false),
    ('pixel-playground',          'Entertainment',   -10.00,  243, false),
    ('spark-electric-solutions',  'Bills',          -100.00,  552, false),
    ('elevate-education',         'Bills',           -50.00,  504, false),
    ('savory-bites-bistro',       'Dining Out',      -55.50,   51, false),
    ('ethan-clark',               'Dining Out',      -32.50,  264, false),
    ('ella-phillips',             'Dining Out',      -45.00,  288, false),
    ('serenity-spa-and-wellness', 'Personal Care',   -30.00,  336, false),
    ('sofia-peterson',            'Personal Care',   -10.00,  192, false),

    -- ── this month: unbudgeted spend ────────────────────────────────────────
    ('daniel-carter',             'General',         -42.30,   72, false),
    ('urban-services-hub',        'General',         -65.00,   99, false),
    ('swift-ride-share',          'Transportation',  -45.00,  144, false),
    ('bytewise',                  'Lifestyle',       -49.99,  168, false),
    ('nimbus-data-storage',       'Lifestyle',        -9.99,  180, false),
    ('green-plate-eatery',        'Groceries',       -38.50,  216, false),
    ('technova-innovations',      'Shopping',      -1111.72,  312, false),

    -- ── last month: history, excluded from this month's totals ──────────────
    ('rina-sato',                 'Entertainment',   -10.00,  240, true),
    ('harper-edwards',            'Dining Out',      -25.00,  120, true),
    ('ecofuel-energy',            'Bills',           -35.00,   72, true),
    ('yuna-kim',                  'General',         200.00,   48, true)
) AS v(slug, category, amount, hours_ago, prev_month)
JOIN public.counterparties c ON c.slug = v.slug
WHERE NOT EXISTS (SELECT 1 FROM public.transactions WHERE user_id = 1);
