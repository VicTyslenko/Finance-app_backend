-- Transaction counterparties: who money went to or came from.
-- Distinct from public.users, which is "accounts that can log in".
-- 30 rows, matching the 30 design assets in public/assets/images/avatars.

CREATE TABLE IF NOT EXISTS public.counterparties (
    counterparty_id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name       varchar(255) NOT NULL UNIQUE,
    slug       varchar(255) NOT NULL UNIQUE,
    avatar_url text NOT NULL,
    kind       text NOT NULL CHECK (kind IN ('person', 'business')),
    created_at timestamptz NOT NULL DEFAULT now()
);

INSERT INTO public.counterparties (name, slug, kind, avatar_url)
SELECT v.name, v.slug, v.kind, '/assets/images/avatars/' || v.slug || '.jpg'
FROM (VALUES
    ('Aqua Flow Utilities',       'aqua-flow-utilities',       'business'),
    ('Buzz Marketing Group',      'buzz-marketing-group',      'business'),
    ('ByteWise',                  'bytewise',                  'business'),
    ('Daniel Carter',             'daniel-carter',             'person'),
    ('EcoFuel Energy',            'ecofuel-energy',            'business'),
    ('Elevate Education',         'elevate-education',         'business'),
    ('Ella Phillips',             'ella-phillips',             'person'),
    ('Emma Richardson',           'emma-richardson',           'person'),
    ('Ethan Clark',               'ethan-clark',               'person'),
    ('Flavor Fiesta',             'flavor-fiesta',             'business'),
    ('Green Plate Eatery',        'green-plate-eatery',        'business'),
    ('Harper Edwards',            'harper-edwards',            'person'),
    ('James Thompson',            'james-thompson',            'person'),
    ('Liam Hughes',               'liam-hughes',               'person'),
    ('Lily Ramirez',              'lily-ramirez',              'person'),
    ('Mason Martinez',            'mason-martinez',            'person'),
    ('Nimbus Data Storage',       'nimbus-data-storage',       'business'),
    ('Pixel Playground',          'pixel-playground',          'business'),
    ('Rina Sato',                 'rina-sato',                 'person'),
    ('Savory Bites Bistro',       'savory-bites-bistro',       'business'),
    ('Sebastian Cook',            'sebastian-cook',            'person'),
    ('Serenity Spa & Wellness',   'serenity-spa-and-wellness', 'business'),
    ('Sofia Peterson',            'sofia-peterson',            'person'),
    ('Spark Electric Solutions',  'spark-electric-solutions',  'business'),
    ('Sun Park',                  'sun-park',                  'person'),
    ('Swift Ride Share',          'swift-ride-share',          'business'),
    ('TechNova Innovations',      'technova-innovations',      'business'),
    ('Urban Services Hub',        'urban-services-hub',        'business'),
    ('William Harris',            'william-harris',            'person'),
    ('Yuna Kim',                  'yuna-kim',                  'person')
) AS v(name, slug, kind)
ON CONFLICT (slug) DO NOTHING;
