CREATE TABLE IF NOT EXISTS public.users(
   user_id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
   email varchar(255) NOT NULL UNIQUE,
   full_name varchar(255) NOT NULL,
   created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS public.prices(
    price_id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id integer NOT NULL REFERENCES public.users(user_id) ON DELETE CASCADE,
    label varchar(255) NOT NULL,
    amount numeric(12,2) NOT NULL,
    currency char(3) NOT NULL DEFAULT 'GBP',
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS ix_prices_user ON public.prices (user_id);
