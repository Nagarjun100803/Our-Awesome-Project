-- educational-details
-- depends: 20260806_01_rikl9-personal-details

-- migrate: apply

CREATE TABLE IF NOT EXISTS academic_details(
    id UUID REFERENCES users(id) NOT NULL,
    level_of_education VARCHAR(100) NOT NULL,
    institution_name VARCHAR(255) NOT NULL,
    board_university VARCHAR(255) NOT NULL,
    course_stream_specialization VARCHAR(255),
    year_of_passing VARCHAR(5) NOT NULL,
    register_number VARCHAR(100),
    current_semester NUMERIC(2),
    grading_system VARCHAR(50),
    score NUMERIC(3,3),
    currently_enrolled BOOLEAN NOT NULL DEFAULT FALSE,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ,
    deleted_at TIMESTAMPTZ,
    created_by UUID REFERENCES users(id) NOT NULL,
    updated_by UUID REFERENCES users(id),
    deleted_by UUID REFERENCES users(id)
);


-- migrate: rollback

DROP TABLE IF EXISTS academic_details;
