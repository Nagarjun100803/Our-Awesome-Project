-- Providers Table
-- depends: 20260730_01_2l8nb-users-table

-- migrate: apply
CREATE TABLE IF NOT EXISTS providers (
    name VARCHAR(255) NOT NULL,
    user_id UUID REFERENCES users(id),
    sub VARCHAR(255),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    deleted_at TIMESTAMPTZ
);


-- migrate: rollback

DROP TABLE IF EXISTS providers;
