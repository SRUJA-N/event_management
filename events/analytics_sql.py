"""
Analytics helpers executed with ``connection.cursor()`` as required.
"""
from __future__ import annotations

from typing import Any

from django.db import connection


def fetch_budget_variance_rows() -> list[dict[str, Any]]:
    """
    Raw SQL dashboard: compare College Fund vs Sponsorship and compute variance metrics.

    Variance is defined as (college_fund - sponsorship) relative to total allocation.
    """
    sql = """
        SELECT
            e.id AS event_id,
            e.title,
            e.event_date,
            e.status,
            e.college_fund,
            e.sponsorship,
            (e.college_fund + e.sponsorship) AS total_budget,
            (e.college_fund - e.sponsorship) AS absolute_variance,
            CASE
                WHEN (e.college_fund + e.sponsorship) = 0 THEN 0
                ELSE ROUND(
                    ((e.college_fund - e.sponsorship) / (e.college_fund + e.sponsorship)) * 100,
                    2
                )
            END AS variance_pct
        FROM cse_icb_events e
        WHERE e.status = 'APPROVED'
        ORDER BY e.event_date DESC, e.id DESC
        LIMIT 200;
    """
    with connection.cursor() as cursor:
        cursor.execute(sql)
        cols = [c[0] for c in cursor.description]
        rows = []
        for record in cursor.fetchall():
            item = dict(zip(cols, record))
            for key in ("college_fund", "sponsorship", "total_budget", "absolute_variance", "variance_pct"):
                if key in item and item[key] is not None and not isinstance(item[key], (int, float)):
                    item[key] = float(item[key])
            rows.append(item)
    return rows


def student_usn_exists_raw(usn: str) -> tuple[bool, int | None]:
    """
    Attendance validation: check Student master via raw SQL before QR registration.
    Returns (exists, student_id).
    """
    normalized = usn.strip().upper()
    sql = "SELECT id FROM cse_icb_students WHERE usn = %s LIMIT 1;"
    with connection.cursor() as cursor:
        cursor.execute(sql, [normalized])
        row = cursor.fetchone()
    if not row:
        return False, None
    return True, int(row[0])
