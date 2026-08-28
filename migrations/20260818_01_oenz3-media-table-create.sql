-- media table - create
-- depends: 20260811_01_85uyu-parental-details

-- migrate: apply
CREATE TABLE IF NOT EXISTS media (
    id UUID PRIMARY KEY default gen_random_uuid(),
    filename VARCHAR(255) NOT NULL,
    storage_provider VARCHAR(255) NOT NULL,
    storage_key VARCHAR(255) NOT NULL,
    content_type VARCHAR(255) NOT NULL,
    file_size INT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    status VARCHAR(255) NOT NULL DEFAULT 'pending',
    created_by UUID NOT NULL REFERENCES users(id),
    updated_at TIMESTAMPTZ,
    updated_by UUID REFERENCES users(id),
    deleted_at TIMESTAMPTZ,
    deleted_by UUID REFERENCES users(id)
);

-- migrate: rollback

DROP TABLE IF EXISTS media;
