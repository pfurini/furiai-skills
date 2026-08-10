CREATE TABLE plans (
    id             INTEGER PRIMARY KEY,
    name           TEXT NOT NULL,
    price_cents    INTEGER NOT NULL,
    billing_period TEXT NOT NULL CHECK (billing_period IN ('monthly', 'annual'))
);
