-- personal-details
-- depends: 20260730_02_k9z7d-providers-table

-- migrate: apply

CREATE TABLE IF NOT EXISTS personal_details(
    id UUID PRIMARY KEY REFERENCES users(id),
    dob DATE NOT NULL,
    gender VARCHAR(10) NOT NULL,
    nationality VARCHAR(50) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    alternate_phone VARCHAR(20),
    street VARCHAR(255) NOT NULL,
    city VARCHAR(100) NOT NULL,
    district VARCHAR(70) NOT NULL,
    state VARCHAR(50) NOT NULL,
    country VARCHAR(50) NOT NULL,
    pincode VARCHAR(20) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ,
    deleted_at TIMESTAMPTZ,
    created_by UUID REFERENCES users(id),
    updated_by UUID REFERENCES users(id),
    deleted_by UUID REFERENCES users(id)
);

-- migrate: rollback
DROP TABLE IF EXISTS personal_details;
