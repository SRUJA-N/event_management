"""Generate ``init.sql`` with 120+ students and multi-year seeded events."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "init.sql"


def main() -> None:
    lines: list[str] = []
    lines.append("SET NAMES utf8mb4;\n")
    lines.append("-- Idempotent cleanup for re-seeding demo events\n")
    lines.append("DELETE a FROM cse_icb_attendance a JOIN cse_icb_events e ON e.id = a.event_id WHERE e.slug LIKE 'seed-%';\n")
    lines.append("DELETE bh FROM cse_icb_budget_history bh JOIN cse_icb_events e ON e.id = bh.event_id WHERE e.slug LIKE 'seed-%';\n")
    lines.append("DELETE FROM cse_icb_events WHERE slug LIKE 'seed-%';\n\n")

    students = []
    for i in range(1, 121):
        usn = f"1BIT21CS{i:03d}"
        name = f"Student {i:03d}"
        sem = 3 + (i % 3)
        students.append(f"('{usn}', '{name}', {sem})")
    lines.append("INSERT IGNORE INTO cse_icb_students (usn, name, semester) VALUES\n")
    lines.append(",\n".join(students) + ";\n\n")

    events: list[tuple[str, str, str, str, int, int, int, str, str, str, str]] = []
    idx = 0
    catalog = [
        # year, month, day, title, etype, venue, parts, college, sponsor, status
        (2024, 2, 18, "IoT Summit 2024", "IOT", "Auditorium", 180, 65000, 42000, "APPROVED"),
        (2024, 4, 6, "Blockchain Governance Forum", "BLOCKCHAIN", "Seminar Hall A", 95, 47000, 53000, "APPROVED"),
        (2024, 6, 12, "Cyber Range Challenge", "CYBER", "Cyber Range", 140, 72000, 31000, "APPROVED"),
        (2024, 8, 24, "IoT Sensors Hacknight", "IOT", "IoT Lab", 75, 28000, 12000, "PENDING"),
        (2024, 10, 3, "Crypto Policy Debate", "BLOCKCHAIN", "Auditorium", 60, 22000, 8000, "REJECTED"),
        (2025, 1, 21, "Industrial IoT Colloquium", "IOT", "Main Auditorium", 170, 61000, 45000, "APPROVED"),
        (2025, 3, 9, "Smart Contracts Studio", "BLOCKCHAIN", "Incubation Center", 88, 39000, 41000, "APPROVED"),
        (2025, 5, 17, "Blue Team Workshop", "CYBER", "Lab B-204", 130, 58000, 22000, "APPROVED"),
        (2025, 7, 8, "Threat Hunting Sprint", "CYBER", "Cyber Range", 105, 51000, 19000, "PENDING"),
        (2025, 9, 30, "Blockchain Career Fair", "BLOCKCHAIN", "Open Arena", 220, 80000, 95000, "APPROVED"),
        (2026, 2, 14, "Edge AI + IoT Symposium", "IOT", "Auditorium", 210, 88000, 67000, "APPROVED"),
        (2026, 4, 28, "Post-Quantum Readiness", "CYBER", "Seminar Hall B", 125, 64000, 36000, "APPROVED"),
        (2026, 6, 6, "DeFi Risk Lab", "BLOCKCHAIN", "Lab C-105", 70, 33000, 27000, "PENDING"),
        (2026, 8, 19, "Campus IoT Telemetry", "IOT", "IoT Innovation Lab", 145, 54000, 33000, "APPROVED"),
        (2026, 10, 11, "SOC Automation Day", "CYBER", "Cyber Range", 155, 69000, 41000, "APPROVED"),
    ]
    for tup in catalog:
        year, month, day = tup[0], tup[1], tup[2]
        title, etype, venue, parts, cf, sp, status = tup[3:]
        idx += 1
        slug = f"seed-{year}-{idx:02d}-{etype.lower()}"
        token = f"{idx:02d}{year}{'abcdef0123456789'}"[:32]
        date_iso = f"{year:04d}-{month:02d}-{day:02d}"
        events.append((slug, f"[SEED] {title}", etype, venue, parts, cf, sp, status, date_iso, token, ""))

    lines.append("-- Seeded events (2024-2026) referencing demo faculty/admin accounts\n")
    for slug, title, etype, venue, parts, cf, sp, status, date_iso, token, _note in events:
        approved_sql = "NULL" if status != "APPROVED" else "(SELECT id FROM cse_icb_users WHERE username='admin_demo' LIMIT 1)"
        approved_at_sql = "NULL" if status != "APPROVED" else "NOW()"
        token_sql = "''" if status != "APPROVED" else f"'{token}'"
        rej = "Not aligned with semester plan" if status == "REJECTED" else ""
        lines.append(
            "INSERT INTO cse_icb_events (\n"
            "  title, slug, event_type, venue, expected_participants, college_fund, sponsorship,\n"
            "  status, event_date, description, created_by_id, approved_by_id, approved_at,\n"
            "  rejected_reason, attendance_token, created_at, updated_at\n"
            ") VALUES (\n"
            f"  '{title}', '{slug}', '{etype}', '{venue}', {parts}, {cf}, {sp},\n"
            f"  '{status}', '{date_iso}', 'Synthetic departmental seed row',\n"
            "  (SELECT id FROM cse_icb_users WHERE username='faculty_demo' LIMIT 1),\n"
            f"  {approved_sql},\n"
            f"  {approved_at_sql},\n"
            f"  '{rej}', {token_sql}, NOW(), NOW()\n"
            ");\n\n"
        )

    lines.append(
        "-- Snapshot history for approved seeded events\n"
        "INSERT INTO cse_icb_budget_history (event_id, college_fund, sponsorship, note, recorded_at)\n"
        "SELECT e.id, e.college_fund, e.sponsorship, 'Seed snapshot', NOW()\n"
        "FROM cse_icb_events e\n"
        "WHERE e.slug LIKE 'seed-%' AND e.status = 'APPROVED';\n\n"
    )

    lines.append(
        "-- Sample attendance links (first three students on first approved seed event)\n"
        "INSERT IGNORE INTO cse_icb_attendance (event_id, student_id, registered_at)\n"
        "SELECT e.id, s.id, NOW()\n"
        "FROM cse_icb_events e\n"
        "JOIN cse_icb_students s ON s.usn IN ('1BIT21CS001','1BIT21CS002','1BIT21CS003')\n"
        "WHERE e.slug = (\n"
        "  SELECT slug FROM cse_icb_events WHERE slug LIKE 'seed-%' AND status='APPROVED' ORDER BY event_date LIMIT 1\n"
        ");\n"
    )

    OUT.write_text("".join(lines), encoding="utf-8")
    print(f"Wrote {OUT} ({len(lines)} chunks)")


if __name__ == "__main__":
    main()
