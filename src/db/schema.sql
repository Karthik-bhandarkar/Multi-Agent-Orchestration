PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS students (
    student_id INTEGER PRIMARY KEY AUTOINCREMENT,
    roll_no    TEXT UNIQUE NOT NULL,
    name       TEXT NOT NULL,
    semester   INTEGER NOT NULL CHECK (semester BETWEEN 1 AND 8)
);

CREATE TABLE IF NOT EXISTS subjects (
    subject_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name       TEXT UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS marks (
    mark_id                INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id             INTEGER NOT NULL,
    subject_id             INTEGER NOT NULL,
    score                  REAL NOT NULL CHECK (score >= 0 AND score <= 100),
    attendance_percentage  REAL NOT NULL CHECK (attendance_percentage >= 0 AND attendance_percentage <= 100),
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (subject_id) REFERENCES subjects(subject_id)
);

CREATE INDEX IF NOT EXISTS idx_students_roll_no ON students(roll_no);
CREATE INDEX IF NOT EXISTS idx_marks_student_id ON marks(student_id);

INSERT OR IGNORE INTO students (roll_no, name, semester) VALUES
    ('102', 'Aarav Sharma', 4),
    ('103', 'Priya Nair', 4),
    ('104', 'Rohan Gupta', 4);

INSERT OR IGNORE INTO subjects (name) VALUES
    ('Data Structures'),
    ('Operating Systems'),
    ('Database Management'),
    ('Computer Networks');

INSERT INTO marks (student_id, subject_id, score, attendance_percentage)
SELECT s.student_id, sub.subject_id, m.score, m.attendance
FROM students s
JOIN (
    SELECT 'Data Structures' AS subj, 82.0 AS score, 91.0 AS attendance
    UNION ALL SELECT 'Operating Systems', 76.0, 88.0
    UNION ALL SELECT 'Database Management', 90.0, 95.0
    UNION ALL SELECT 'Computer Networks', 68.0, 79.0
) m ON 1=1
JOIN subjects sub ON sub.name = m.subj
WHERE s.roll_no = '102';

INSERT INTO marks (student_id, subject_id, score, attendance_percentage)
SELECT s.student_id, sub.subject_id, m.score, m.attendance
FROM students s
JOIN (
    SELECT 'Data Structures' AS subj, 95.0 AS score, 97.0 AS attendance
    UNION ALL SELECT 'Operating Systems', 88.0, 93.0
    UNION ALL SELECT 'Database Management', 91.0, 96.0
    UNION ALL SELECT 'Computer Networks', 85.0, 90.0
) m ON 1=1
JOIN subjects sub ON sub.name = m.subj
WHERE s.roll_no = '103';

INSERT INTO marks (student_id, subject_id, score, attendance_percentage)
SELECT s.student_id, sub.subject_id, m.score, m.attendance
FROM students s
JOIN (
    SELECT 'Data Structures' AS subj, 35.0 AS score, 60.0 AS attendance
    UNION ALL SELECT 'Operating Systems', 42.0, 65.0
    UNION ALL SELECT 'Database Management', 38.0, 58.0
    UNION ALL SELECT 'Computer Networks', 45.0, 70.0
) m ON 1=1
JOIN subjects sub ON sub.name = m.subj
WHERE s.roll_no = '104';
