-- account verification using student id
-- depends: 20260818_01_oenz3-media-table-create

-- migrate: apply
CREATE TABLE IF NOT EXISTS profile_verification(
    id UUID NOT NULL REFERENCES users(id),
    media_id UUID NOT NULL REFERENCES media(id),
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    remarks TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ,
    deleted_at TIMESTAMPTZ,
    created_by UUID NOT NULL REFERENCES users(id),
    updated_by UUID REFERENCES users(id),
    deleted_by UUID REFERENCES users(id)
);


-- migrate: rollback
DROP TABLE IF EXISTS profile_verification;
