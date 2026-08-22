UPDATE public.users u
SET avatar_url = v.avatar_url
FROM (VALUES
    ('emma.richardson@example.com', '/assets/images/avatars/emma-richardson.jpg'),
    ('daniel.carter@example.com',   '/assets/images/avatars/daniel-carter.jpg'),
    ('sun.park@example.com',        '/assets/images/avatars/sun-park.jpg'),
    ('liam.hughes@example.com',     '/assets/images/avatars/liam-hughes.jpg'),
    ('lily.ramirez@example.com',    '/assets/images/avatars/lily-ramirez.jpg'),
    ('ethan.clark@example.com',     '/assets/images/avatars/ethan-clark.jpg'),
    ('james.thompson@example.com',  '/assets/images/avatars/james-thompson.jpg')
) AS v(email, avatar_url)
WHERE u.email = v.email
  AND u.avatar_url IS NULL;