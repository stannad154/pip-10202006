
CREATE TABLE IF NOT EXISTS students (
    id SERIAL PRIMARY KEY,
    netid VARCHAR(100),
    name VARCHAR(255),
    school_year VARCHAR(100),
    intro_programming TEXT,
    skill_programming TEXT,
    skill_data_stats TEXT,
    skill_frontend_design TEXT,
    skill_business_pitch TEXT,
    tools TEXT,
    availability TEXT,
    working_style TEXT,
    interests TEXT,
    semester_goal TEXT,
    submitted_at TEXT
);
