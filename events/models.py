from __future__ import annotations

import uuid

from django.conf import settings
from django.db import models


class Student(models.Model):
    """CSE-ICB student master (3NF: USN is business key)."""

    usn = models.CharField(max_length=20, unique=True, db_index=True)
    name = models.CharField(max_length=200)
    semester = models.PositiveSmallIntegerField()

    class Meta:
        db_table = "cse_icb_students"
        ordering = ["usn"]

    def __str__(self) -> str:
        return f"{self.usn} — {self.name}"


class Event(models.Model):
    """Department event with approval workflow and budget split."""

    class EventType(models.TextChoices):
        IOT = "IOT", "IoT"
        BLOCKCHAIN = "BLOCKCHAIN", "Blockchain"
        CYBER = "CYBER", "Cyber Security"

    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending approval"
        APPROVED = "APPROVED", "Approved"
        REJECTED = "REJECTED", "Rejected"

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=280, unique=True)
    event_type = models.CharField(max_length=32, choices=EventType.choices)
    venue = models.CharField(max_length=200)
    expected_participants = models.PositiveIntegerField(default=0)
    college_fund = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    sponsorship = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    event_date = models.DateField()
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="events_created",
    )
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="events_approved",
    )
    approved_at = models.DateTimeField(null=True, blank=True)
    rejected_reason = models.TextField(blank=True)
    attendance_token = models.CharField(max_length=64, blank=True, db_index=True)

    class Meta:
        db_table = "cse_icb_events"
        ordering = ["-event_date", "-id"]

    def __str__(self) -> str:
        return self.title

    @property
    def is_locked(self) -> bool:
        """Approved events are immutable for budget fields and publicly visible to viewers."""
        return self.status == self.Status.APPROVED

    @property
    def can_issue_qr(self) -> bool:
        return self.status == self.Status.APPROVED and bool(self.attendance_token)

    def assign_attendance_token_if_missing(self) -> None:
        if self.status == self.Status.APPROVED and not self.attendance_token:
            self.attendance_token = uuid.uuid4().hex


class Attendance(models.Model):
    """Attendance fact table (3NF: references Event and Student only)."""

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="attendance_rows")
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="attendance_rows")
    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "cse_icb_attendance"
        ordering = ["-registered_at"]
        constraints = [
            models.UniqueConstraint(fields=["event", "student"], name="uniq_cse_icb_attendance_event_student"),
        ]


class BudgetHistory(models.Model):
    """Point-in-time budget snapshots for analytics and audit trail."""

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="budget_snapshots")
    recorded_at = models.DateTimeField(auto_now_add=True)
    college_fund = models.DecimalField(max_digits=12, decimal_places=2)
    sponsorship = models.DecimalField(max_digits=12, decimal_places=2)
    note = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = "cse_icb_budget_history"
        ordering = ["-recorded_at"]
