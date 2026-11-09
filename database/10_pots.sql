ALTER TABLE public.users ADD COLUMN IF NOT EXISTS balance numeric(12,2) NOT NULL DEFAULT 0;


CREATE TABLE IF NOT EXISTS public.pots (
    pot_id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id integer NOT NULL REFERENCES public.users(user_id) ON DELETE CASCADE,
    name varchar(255) NOT NULL,
    target numeric(12,2) NOT NULL CHECK (target > 0),
    total numeric(12,2) NOT NULL DEFAULT 0 CHECK (total >= 0),
    theme text NOT NULL,
    created_at timestamptz NOT NULL DEFAULT now(),
    UNIQUE (user_id, name)
);

