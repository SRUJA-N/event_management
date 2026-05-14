SET NAMES utf8mb4;
-- Idempotent cleanup for re-seeding demo events
DELETE a FROM cse_icb_attendance a JOIN cse_icb_events e ON e.id = a.event_id WHERE e.slug LIKE 'seed-%';
DELETE bh FROM cse_icb_budget_history bh JOIN cse_icb_events e ON e.id = bh.event_id WHERE e.slug LIKE 'seed-%';
DELETE FROM cse_icb_events WHERE slug LIKE 'seed-%';

INSERT IGNORE INTO cse_icb_students (usn, name, semester) VALUES
('1BIT21CS001', 'Student 001', 4),
('1BIT21CS002', 'Student 002', 5),
('1BIT21CS003', 'Student 003', 3),
('1BIT21CS004', 'Student 004', 4),
('1BIT21CS005', 'Student 005', 5),
('1BIT21CS006', 'Student 006', 3),
('1BIT21CS007', 'Student 007', 4),
('1BIT21CS008', 'Student 008', 5),
('1BIT21CS009', 'Student 009', 3),
('1BIT21CS010', 'Student 010', 4),
('1BIT21CS011', 'Student 011', 5),
('1BIT21CS012', 'Student 012', 3),
('1BIT21CS013', 'Student 013', 4),
('1BIT21CS014', 'Student 014', 5),
('1BIT21CS015', 'Student 015', 3),
('1BIT21CS016', 'Student 016', 4),
('1BIT21CS017', 'Student 017', 5),
('1BIT21CS018', 'Student 018', 3),
('1BIT21CS019', 'Student 019', 4),
('1BIT21CS020', 'Student 020', 5),
('1BIT21CS021', 'Student 021', 3),
('1BIT21CS022', 'Student 022', 4),
('1BIT21CS023', 'Student 023', 5),
('1BIT21CS024', 'Student 024', 3),
('1BIT21CS025', 'Student 025', 4),
('1BIT21CS026', 'Student 026', 5),
('1BIT21CS027', 'Student 027', 3),
('1BIT21CS028', 'Student 028', 4),
('1BIT21CS029', 'Student 029', 5),
('1BIT21CS030', 'Student 030', 3),
('1BIT21CS031', 'Student 031', 4),
('1BIT21CS032', 'Student 032', 5),
('1BIT21CS033', 'Student 033', 3),
('1BIT21CS034', 'Student 034', 4),
('1BIT21CS035', 'Student 035', 5),
('1BIT21CS036', 'Student 036', 3),
('1BIT21CS037', 'Student 037', 4),
('1BIT21CS038', 'Student 038', 5),
('1BIT21CS039', 'Student 039', 3),
('1BIT21CS040', 'Student 040', 4),
('1BIT21CS041', 'Student 041', 5),
('1BIT21CS042', 'Student 042', 3),
('1BIT21CS043', 'Student 043', 4),
('1BIT21CS044', 'Student 044', 5),
('1BIT21CS045', 'Student 045', 3),
('1BIT21CS046', 'Student 046', 4),
('1BIT21CS047', 'Student 047', 5),
('1BIT21CS048', 'Student 048', 3),
('1BIT21CS049', 'Student 049', 4),
('1BIT21CS050', 'Student 050', 5),
('1BIT21CS051', 'Student 051', 3),
('1BIT21CS052', 'Student 052', 4),
('1BIT21CS053', 'Student 053', 5),
('1BIT21CS054', 'Student 054', 3),
('1BIT21CS055', 'Student 055', 4),
('1BIT21CS056', 'Student 056', 5),
('1BIT21CS057', 'Student 057', 3),
('1BIT21CS058', 'Student 058', 4),
('1BIT21CS059', 'Student 059', 5),
('1BIT21CS060', 'Student 060', 3),
('1BIT21CS061', 'Student 061', 4),
('1BIT21CS062', 'Student 062', 5),
('1BIT21CS063', 'Student 063', 3),
('1BIT21CS064', 'Student 064', 4),
('1BIT21CS065', 'Student 065', 5),
('1BIT21CS066', 'Student 066', 3),
('1BIT21CS067', 'Student 067', 4),
('1BIT21CS068', 'Student 068', 5),
('1BIT21CS069', 'Student 069', 3),
('1BIT21CS070', 'Student 070', 4),
('1BIT21CS071', 'Student 071', 5),
('1BIT21CS072', 'Student 072', 3),
('1BIT21CS073', 'Student 073', 4),
('1BIT21CS074', 'Student 074', 5),
('1BIT21CS075', 'Student 075', 3),
('1BIT21CS076', 'Student 076', 4),
('1BIT21CS077', 'Student 077', 5),
('1BIT21CS078', 'Student 078', 3),
('1BIT21CS079', 'Student 079', 4),
('1BIT21CS080', 'Student 080', 5),
('1BIT21CS081', 'Student 081', 3),
('1BIT21CS082', 'Student 082', 4),
('1BIT21CS083', 'Student 083', 5),
('1BIT21CS084', 'Student 084', 3),
('1BIT21CS085', 'Student 085', 4),
('1BIT21CS086', 'Student 086', 5),
('1BIT21CS087', 'Student 087', 3),
('1BIT21CS088', 'Student 088', 4),
('1BIT21CS089', 'Student 089', 5),
('1BIT21CS090', 'Student 090', 3),
('1BIT21CS091', 'Student 091', 4),
('1BIT21CS092', 'Student 092', 5),
('1BIT21CS093', 'Student 093', 3),
('1BIT21CS094', 'Student 094', 4),
('1BIT21CS095', 'Student 095', 5),
('1BIT21CS096', 'Student 096', 3),
('1BIT21CS097', 'Student 097', 4),
('1BIT21CS098', 'Student 098', 5),
('1BIT21CS099', 'Student 099', 3),
('1BIT21CS100', 'Student 100', 4),
('1BIT21CS101', 'Student 101', 5),
('1BIT21CS102', 'Student 102', 3),
('1BIT21CS103', 'Student 103', 4),
('1BIT21CS104', 'Student 104', 5),
('1BIT21CS105', 'Student 105', 3),
('1BIT21CS106', 'Student 106', 4),
('1BIT21CS107', 'Student 107', 5),
('1BIT21CS108', 'Student 108', 3),
('1BIT21CS109', 'Student 109', 4),
('1BIT21CS110', 'Student 110', 5),
('1BIT21CS111', 'Student 111', 3),
('1BIT21CS112', 'Student 112', 4),
('1BIT21CS113', 'Student 113', 5),
('1BIT21CS114', 'Student 114', 3),
('1BIT21CS115', 'Student 115', 4),
('1BIT21CS116', 'Student 116', 5),
('1BIT21CS117', 'Student 117', 3),
('1BIT21CS118', 'Student 118', 4),
('1BIT21CS119', 'Student 119', 5),
('1BIT21CS120', 'Student 120', 3);

-- Seeded events (2024-2026) referencing demo faculty/admin accounts
INSERT INTO cse_icb_events (
  title, slug, event_type, venue, expected_participants, college_fund, sponsorship,
  status, event_date, description, created_by_id, approved_by_id, approved_at,
  rejected_reason, attendance_token, created_at, updated_at
) VALUES (
  '[SEED] IoT Summit 2024', 'seed-2024-01-iot', 'IOT', 'Auditorium', 180, 65000, 42000,
  'APPROVED', '2024-02-18', 'Synthetic departmental seed row',
  (SELECT id FROM cse_icb_users WHERE username='faculty_demo' LIMIT 1),
  (SELECT id FROM cse_icb_users WHERE username='admin_demo' LIMIT 1),
  NOW(),
  '', '012024abcdef0123456789', NOW(), NOW()
);

INSERT INTO cse_icb_events (
  title, slug, event_type, venue, expected_participants, college_fund, sponsorship,
  status, event_date, description, created_by_id, approved_by_id, approved_at,
  rejected_reason, attendance_token, created_at, updated_at
) VALUES (
  '[SEED] Blockchain Governance Forum', 'seed-2024-02-blockchain', 'BLOCKCHAIN', 'Seminar Hall A', 95, 47000, 53000,
  'APPROVED', '2024-04-06', 'Synthetic departmental seed row',
  (SELECT id FROM cse_icb_users WHERE username='faculty_demo' LIMIT 1),
  (SELECT id FROM cse_icb_users WHERE username='admin_demo' LIMIT 1),
  NOW(),
  '', '022024abcdef0123456789', NOW(), NOW()
);

INSERT INTO cse_icb_events (
  title, slug, event_type, venue, expected_participants, college_fund, sponsorship,
  status, event_date, description, created_by_id, approved_by_id, approved_at,
  rejected_reason, attendance_token, created_at, updated_at
) VALUES (
  '[SEED] Cyber Range Challenge', 'seed-2024-03-cyber', 'CYBER', 'Cyber Range', 140, 72000, 31000,
  'APPROVED', '2024-06-12', 'Synthetic departmental seed row',
  (SELECT id FROM cse_icb_users WHERE username='faculty_demo' LIMIT 1),
  (SELECT id FROM cse_icb_users WHERE username='admin_demo' LIMIT 1),
  NOW(),
  '', '032024abcdef0123456789', NOW(), NOW()
);

INSERT INTO cse_icb_events (
  title, slug, event_type, venue, expected_participants, college_fund, sponsorship,
  status, event_date, description, created_by_id, approved_by_id, approved_at,
  rejected_reason, attendance_token, created_at, updated_at
) VALUES (
  '[SEED] IoT Sensors Hacknight', 'seed-2024-04-iot', 'IOT', 'IoT Lab', 75, 28000, 12000,
  'PENDING', '2024-08-24', 'Synthetic departmental seed row',
  (SELECT id FROM cse_icb_users WHERE username='faculty_demo' LIMIT 1),
  NULL,
  NULL,
  '', '', NOW(), NOW()
);

INSERT INTO cse_icb_events (
  title, slug, event_type, venue, expected_participants, college_fund, sponsorship,
  status, event_date, description, created_by_id, approved_by_id, approved_at,
  rejected_reason, attendance_token, created_at, updated_at
) VALUES (
  '[SEED] Crypto Policy Debate', 'seed-2024-05-blockchain', 'BLOCKCHAIN', 'Auditorium', 60, 22000, 8000,
  'REJECTED', '2024-10-03', 'Synthetic departmental seed row',
  (SELECT id FROM cse_icb_users WHERE username='faculty_demo' LIMIT 1),
  NULL,
  NULL,
  'Not aligned with semester plan', '', NOW(), NOW()
);

INSERT INTO cse_icb_events (
  title, slug, event_type, venue, expected_participants, college_fund, sponsorship,
  status, event_date, description, created_by_id, approved_by_id, approved_at,
  rejected_reason, attendance_token, created_at, updated_at
) VALUES (
  '[SEED] Industrial IoT Colloquium', 'seed-2025-06-iot', 'IOT', 'Main Auditorium', 170, 61000, 45000,
  'APPROVED', '2025-01-21', 'Synthetic departmental seed row',
  (SELECT id FROM cse_icb_users WHERE username='faculty_demo' LIMIT 1),
  (SELECT id FROM cse_icb_users WHERE username='admin_demo' LIMIT 1),
  NOW(),
  '', '062025abcdef0123456789', NOW(), NOW()
);

INSERT INTO cse_icb_events (
  title, slug, event_type, venue, expected_participants, college_fund, sponsorship,
  status, event_date, description, created_by_id, approved_by_id, approved_at,
  rejected_reason, attendance_token, created_at, updated_at
) VALUES (
  '[SEED] Smart Contracts Studio', 'seed-2025-07-blockchain', 'BLOCKCHAIN', 'Incubation Center', 88, 39000, 41000,
  'APPROVED', '2025-03-09', 'Synthetic departmental seed row',
  (SELECT id FROM cse_icb_users WHERE username='faculty_demo' LIMIT 1),
  (SELECT id FROM cse_icb_users WHERE username='admin_demo' LIMIT 1),
  NOW(),
  '', '072025abcdef0123456789', NOW(), NOW()
);

INSERT INTO cse_icb_events (
  title, slug, event_type, venue, expected_participants, college_fund, sponsorship,
  status, event_date, description, created_by_id, approved_by_id, approved_at,
  rejected_reason, attendance_token, created_at, updated_at
) VALUES (
  '[SEED] Blue Team Workshop', 'seed-2025-08-cyber', 'CYBER', 'Lab B-204', 130, 58000, 22000,
  'APPROVED', '2025-05-17', 'Synthetic departmental seed row',
  (SELECT id FROM cse_icb_users WHERE username='faculty_demo' LIMIT 1),
  (SELECT id FROM cse_icb_users WHERE username='admin_demo' LIMIT 1),
  NOW(),
  '', '082025abcdef0123456789', NOW(), NOW()
);

INSERT INTO cse_icb_events (
  title, slug, event_type, venue, expected_participants, college_fund, sponsorship,
  status, event_date, description, created_by_id, approved_by_id, approved_at,
  rejected_reason, attendance_token, created_at, updated_at
) VALUES (
  '[SEED] Threat Hunting Sprint', 'seed-2025-09-cyber', 'CYBER', 'Cyber Range', 105, 51000, 19000,
  'PENDING', '2025-07-08', 'Synthetic departmental seed row',
  (SELECT id FROM cse_icb_users WHERE username='faculty_demo' LIMIT 1),
  NULL,
  NULL,
  '', '', NOW(), NOW()
);

INSERT INTO cse_icb_events (
  title, slug, event_type, venue, expected_participants, college_fund, sponsorship,
  status, event_date, description, created_by_id, approved_by_id, approved_at,
  rejected_reason, attendance_token, created_at, updated_at
) VALUES (
  '[SEED] Blockchain Career Fair', 'seed-2025-10-blockchain', 'BLOCKCHAIN', 'Open Arena', 220, 80000, 95000,
  'APPROVED', '2025-09-30', 'Synthetic departmental seed row',
  (SELECT id FROM cse_icb_users WHERE username='faculty_demo' LIMIT 1),
  (SELECT id FROM cse_icb_users WHERE username='admin_demo' LIMIT 1),
  NOW(),
  '', '102025abcdef0123456789', NOW(), NOW()
);

INSERT INTO cse_icb_events (
  title, slug, event_type, venue, expected_participants, college_fund, sponsorship,
  status, event_date, description, created_by_id, approved_by_id, approved_at,
  rejected_reason, attendance_token, created_at, updated_at
) VALUES (
  '[SEED] Edge AI + IoT Symposium', 'seed-2026-11-iot', 'IOT', 'Auditorium', 210, 88000, 67000,
  'APPROVED', '2026-02-14', 'Synthetic departmental seed row',
  (SELECT id FROM cse_icb_users WHERE username='faculty_demo' LIMIT 1),
  (SELECT id FROM cse_icb_users WHERE username='admin_demo' LIMIT 1),
  NOW(),
  '', '112026abcdef0123456789', NOW(), NOW()
);

INSERT INTO cse_icb_events (
  title, slug, event_type, venue, expected_participants, college_fund, sponsorship,
  status, event_date, description, created_by_id, approved_by_id, approved_at,
  rejected_reason, attendance_token, created_at, updated_at
) VALUES (
  '[SEED] Post-Quantum Readiness', 'seed-2026-12-cyber', 'CYBER', 'Seminar Hall B', 125, 64000, 36000,
  'APPROVED', '2026-04-28', 'Synthetic departmental seed row',
  (SELECT id FROM cse_icb_users WHERE username='faculty_demo' LIMIT 1),
  (SELECT id FROM cse_icb_users WHERE username='admin_demo' LIMIT 1),
  NOW(),
  '', '122026abcdef0123456789', NOW(), NOW()
);

INSERT INTO cse_icb_events (
  title, slug, event_type, venue, expected_participants, college_fund, sponsorship,
  status, event_date, description, created_by_id, approved_by_id, approved_at,
  rejected_reason, attendance_token, created_at, updated_at
) VALUES (
  '[SEED] DeFi Risk Lab', 'seed-2026-13-blockchain', 'BLOCKCHAIN', 'Lab C-105', 70, 33000, 27000,
  'PENDING', '2026-06-06', 'Synthetic departmental seed row',
  (SELECT id FROM cse_icb_users WHERE username='faculty_demo' LIMIT 1),
  NULL,
  NULL,
  '', '', NOW(), NOW()
);

INSERT INTO cse_icb_events (
  title, slug, event_type, venue, expected_participants, college_fund, sponsorship,
  status, event_date, description, created_by_id, approved_by_id, approved_at,
  rejected_reason, attendance_token, created_at, updated_at
) VALUES (
  '[SEED] Campus IoT Telemetry', 'seed-2026-14-iot', 'IOT', 'IoT Innovation Lab', 145, 54000, 33000,
  'APPROVED', '2026-08-19', 'Synthetic departmental seed row',
  (SELECT id FROM cse_icb_users WHERE username='faculty_demo' LIMIT 1),
  (SELECT id FROM cse_icb_users WHERE username='admin_demo' LIMIT 1),
  NOW(),
  '', '142026abcdef0123456789', NOW(), NOW()
);

INSERT INTO cse_icb_events (
  title, slug, event_type, venue, expected_participants, college_fund, sponsorship,
  status, event_date, description, created_by_id, approved_by_id, approved_at,
  rejected_reason, attendance_token, created_at, updated_at
) VALUES (
  '[SEED] SOC Automation Day', 'seed-2026-15-cyber', 'CYBER', 'Cyber Range', 155, 69000, 41000,
  'APPROVED', '2026-10-11', 'Synthetic departmental seed row',
  (SELECT id FROM cse_icb_users WHERE username='faculty_demo' LIMIT 1),
  (SELECT id FROM cse_icb_users WHERE username='admin_demo' LIMIT 1),
  NOW(),
  '', '152026abcdef0123456789', NOW(), NOW()
);

-- Snapshot history for approved seeded events
INSERT INTO cse_icb_budget_history (event_id, college_fund, sponsorship, note, recorded_at)
SELECT e.id, e.college_fund, e.sponsorship, 'Seed snapshot', NOW()
FROM cse_icb_events e
WHERE e.slug LIKE 'seed-%' AND e.status = 'APPROVED';

-- Sample attendance links (first three students on first approved seed event)
INSERT IGNORE INTO cse_icb_attendance (event_id, student_id, registered_at)
SELECT e.id, s.id, NOW()
FROM cse_icb_events e
JOIN cse_icb_students s ON s.usn IN ('1BIT21CS001','1BIT21CS002','1BIT21CS003')
WHERE e.slug = (
  SELECT slug FROM cse_icb_events WHERE slug LIKE 'seed-%' AND status='APPROVED' ORDER BY event_date LIMIT 1
);
