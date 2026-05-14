from __future__ import annotations

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    help = "Create demo department accounts used by init.sql (idempotent)."

    def handle(self, *args, **options) -> None:
        demos = [
            ("admin_demo", User.Role.ADMIN, True, True),
            ("faculty_demo", User.Role.FACULTY, False, True),
            ("coordinator_demo", User.Role.STUDENT_COORDINATOR, False, True),
            ("viewer_demo", User.Role.VIEWER, False, True),
        ]
        password = "demo12345"
        for username, role, is_staff, is_active in demos:
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    "email": f"{username}@bit.local",
                    "role": role,
                    "is_staff": is_staff,
                    "is_active": is_active,
                },
            )
            if created:
                user.set_password(password)
                user.save()
                self.stdout.write(self.style.SUCCESS(f"Created {username}"))
            else:
                # keep password predictable for local demos
                user.set_password(password)
                user.role = role
                user.is_staff = is_staff
                user.is_active = is_active
                user.save()
                self.stdout.write(self.style.WARNING(f"Reset {username}"))

        self.stdout.write(self.style.SUCCESS("Demo password for all accounts: demo12345"))
