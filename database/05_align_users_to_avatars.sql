UPDATE public.users u
SET full_name  = v.full_name,
    email      = v.new_email,
    avatar_url = '/assets/images/avatars/' || v.slug || '.jpg'
FROM (VALUES
    ('sofia.almeida@example.com',   'sofia.peterson@example.com',   'Sofia Peterson',  'sofia-peterson'),
    ('noah.bennett@example.com',    'sebastian.cook@example.com',   'Sebastian Cook',  'sebastian-cook'),
    ('aisha.khan@example.com',      'rina.sato@example.com',        'Rina Sato',       'rina-sato'),
    ('marcus.webb@example.com',     'mason.martinez@example.com',   'Mason Martinez',  'mason-martinez'),
    ('chloe.dubois@example.com',    'ella.phillips@example.com',    'Ella Phillips',   'ella-phillips'),
    ('rafael.ortiz@example.com',    'william.harris@example.com',   'William Harris',  'william-harris'),
    ('hannah.lindqvist@example.com','harper.edwards@example.com',   'Harper Edwards',  'harper-edwards'),
    ('oliver.nakamura@example.com', 'yuna.kim@example.com',         'Yuna Kim',        'yuna-kim')
) AS v(old_email, new_email, full_name, slug)
WHERE u.email = v.old_email;
