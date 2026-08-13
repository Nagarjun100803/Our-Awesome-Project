-- parental details
-- depends: 20260806_02_k2kbm-educational-details

-- migrate: apply
CREATE TABLE IF NOT EXISTS parental_details(
    id UUID PRIMARY KEY REFERENCES users(id) ,
    father_name VARCHAR(255),
    father_occupation VARCHAR(100),
    father_mobile VARCHAR(20),
    mother_name VARCHAR(255),
    mother_occupation VARCHAR(100),
    mother_mobile VARCHAR(20),
    guardian_name VARCHAR(255),
    guardian_occupation VARCHAR(100),
    guardian_mobile VARCHAR(20),
    annual_family_income VARCHAR(100) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ,
    deleted_at TIMESTAMPTZ,
    created_by UUID REFERENCES users(id) NOT NULL,
    updated_by UUID REFERENCES users(id),
    deleted_by UUID REFERENCES users(id)
);

-- migrate: rollback
DROP TABLE IF EXISTS parental_details;
