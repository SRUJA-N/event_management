from __future__ import annotations

import io
from typing import Any

import json
import qrcode
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import FileResponse, Http404, HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from accounts.models import User

from .analytics_sql import fetch_budget_variance_rows, student_usn_exists_raw
from .certificates import build_certificate_pdf
from .approval_workflow import approve_event, reject_event
from .decorators import ADMIN, APPROVAL_QUEUE_ROLES, COORD, CREATOR_ROLES, FACULTY, VIEWER, role_required
from .forms import EventForm, PredictForm, ScanForm
from .models import Attendance, Event, Student
from .predictor import predict_future_cost, train_from_events


def _visible_events_queryset(user: User):
    qs = Event.objects.select_related("created_by", "approved_by")
    if user.role == VIEWER:
        return qs.filter(status=Event.Status.APPROVED)
    return qs


@login_required
def dashboard(request: HttpRequest) -> HttpResponse:
    user = request.user
    variance_rows = fetch_budget_variance_rows()
    totals = {"college": 0.0, "sponsor": 0.0}
    for row in variance_rows:
        totals["college"] += float(row.get("college_fund") or 0)
        totals["sponsor"] += float(row.get("sponsorship") or 0)

    events = _visible_events_queryset(user)[:12]
    pending_count = (
        Event.objects.filter(status=Event.Status.PENDING).count()
        if user.role in (ADMIN, FACULTY)
        else 0
    )
    model = train_from_events(Event.objects.filter(status=Event.Status.APPROVED))
    chart_rows = variance_rows[:12]
    chart_json = json.dumps(chart_rows, default=str)
    return render(
        request,
        "events/dashboard.html",
        {
            "variance_rows": variance_rows[:8],
            "variance_rows_json": chart_json,
            "totals": totals,
            "events": events,
            "pending_count": pending_count,
            "has_model": model is not None,
        },
    )


@login_required
def event_list(request: HttpRequest) -> HttpResponse:
    events = _visible_events_queryset(request.user)
    return render(request, "events/event_list.html", {"events": events})


@login_required
@role_required(*CREATOR_ROLES)
def event_create(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = EventForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Event submitted for administrative approval.")
            return redirect("events:event_list")
    else:
        form = EventForm(user=request.user)
    return render(request, "events/event_form.html", {"form": form, "title": "Create Event"})


@login_required
def event_detail(request: HttpRequest, pk: int) -> HttpResponse:
    event = get_object_or_404(Event.objects.select_related("created_by", "approved_by"), pk=pk)
    if request.user.role == VIEWER and event.status != Event.Status.APPROVED:
        raise Http404()
    attendance_count = event.attendance_rows.count()
    return render(
        request,
        "events/event_detail.html",
        {"event": event, "attendance_count": attendance_count},
    )


@login_required
@role_required(*CREATOR_ROLES)
def event_edit(request: HttpRequest, pk: int) -> HttpResponse:
    event = get_object_or_404(Event, pk=pk)
    if event.is_locked:
        messages.error(request, "Approved events are locked and cannot be edited.")
        return redirect("events:event_detail", pk=pk)
    if request.user.role in (FACULTY, COORD) and event.created_by_id != request.user.id:
        raise Http404()
    if request.method == "POST":
        form = EventForm(request.POST, instance=event, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Event updated.")
            return redirect("events:event_detail", pk=event.pk)
    else:
        form = EventForm(instance=event, user=request.user)
    return render(request, "events/event_form.html", {"form": form, "title": "Edit Event", "event": event})


@login_required
@role_required(*APPROVAL_QUEUE_ROLES)
def admin_queue(request: HttpRequest) -> HttpResponse:
    pending = Event.objects.filter(status=Event.Status.PENDING).select_related("created_by")
    can_decide = request.user.role == ADMIN
    return render(request, "events/admin_queue.html", {"pending": pending, "can_decide": can_decide})


@login_required
@role_required(ADMIN)
@require_http_methods(["POST"])
def admin_decide(request: HttpRequest, pk: int) -> HttpResponse:
    event = get_object_or_404(Event, pk=pk)
    action = request.POST.get("action")
    reason = (request.POST.get("rejected_reason") or "").strip()
    if action not in {"approve", "reject"}:
        messages.error(request, "Unknown decision.")
        return redirect("events_admin_approvals")
    try:
        if action == "approve":
            approve_event(event, request.user)
            messages.success(request, "Event approved and locked for budgeting.")
        else:
            reject_event(event, reason=reason)
            messages.warning(request, "Event rejected.")
    except ValueError as exc:
        messages.error(request, str(exc))
        return redirect("events_admin_approvals")
    return redirect("events:event_detail", pk=event.pk)


@login_required
@role_required(*CREATOR_ROLES)
def event_qr(request: HttpRequest, pk: int) -> HttpResponse:
    event = get_object_or_404(Event, pk=pk)
    if request.user.role in (FACULTY, COORD) and event.created_by_id != request.user.id:
        raise Http404()
    if not event.can_issue_qr:
        raise Http404()
    url = request.build_absolute_uri(reverse("events:scan_public", args=[event.pk]))
    url = f"{url}?t={event.attendance_token}"
    img = qrcode.make(url, box_size=6, border=2)
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=False, filename=f"event-{event.pk}-qr.png")


@require_http_methods(["GET", "POST"])
def scan_public(request: HttpRequest, event_id: int) -> HttpResponse:
    event = get_object_or_404(Event, pk=event_id)
    token = request.GET.get("t") or request.POST.get("t")
    if event.status != Event.Status.APPROVED or not event.attendance_token or token != event.attendance_token:
        return render(request, "events/scan_invalid.html", status=403)
    if request.method == "POST":
        form = ScanForm(request.POST)
        if form.is_valid():
            usn = form.cleaned_data["usn"]
            exists, student_id = student_usn_exists_raw(usn)
            if not exists or student_id is None:
                messages.error(request, "USN not found in CSE-ICB student registry.")
            else:
                student = Student.objects.get(pk=student_id)
                att, created = Attendance.objects.get_or_create(event=event, student=student)
                if created:
                    messages.success(request, f"Attendance recorded for {student.usn}.")
                else:
                    messages.info(request, "Attendance already registered for this USN.")
            return redirect(f"{reverse('events:scan_public', args=[event.pk])}?t={event.attendance_token}")
    else:
        form = ScanForm()
    return render(
        request,
        "events/scan.html",
        {"form": form, "event": event, "token": event.attendance_token},
    )


@login_required
def predictor_view(request: HttpRequest) -> HttpResponse:
    model = train_from_events(Event.objects.filter(status=Event.Status.APPROVED))
    prediction: dict[str, Any] | None = None
    if request.method == "POST":
        form = PredictForm(request.POST)
        if form.is_valid():
            pred = predict_future_cost(
                model,
                event_type=form.cleaned_data["event_type"],
                expected_participants=form.cleaned_data["expected_participants"],
                venue=form.cleaned_data["venue"],
            )
            prediction = {
                "cost": round(pred.predicted_cost, 2),
                "beta0": round(pred.beta0, 4),
                "beta1": round(pred.beta1, 4),
                "beta2": round(pred.beta2, 4),
            }
    else:
        form = PredictForm()
    return render(
        request,
        "events/predictor.html",
        {"form": form, "prediction": prediction, "has_model": model is not None},
    )


@login_required
def certificate_pdf(request: HttpRequest, pk: int, usn: str) -> HttpResponse:
    event = get_object_or_404(Event, pk=pk)
    if request.user.role == VIEWER:
        raise Http404()
    if event.status != Event.Status.APPROVED:
        raise Http404()
    exists, student_id = student_usn_exists_raw(usn)
    if not exists or student_id is None:
        raise Http404()
    student = Student.objects.get(pk=student_id)
    if not Attendance.objects.filter(event=event, student=student).exists():
        messages.error(request, "Certificate available only after QR attendance is recorded.")
        return redirect("events:event_detail", pk=pk)
    pdf_bytes = build_certificate_pdf(
        student_name=student.name,
        usn=student.usn,
        event_title=event.title,
        event_date=event.event_date.isoformat(),
    )
    filename = f"certificate-{student.usn}-{event.pk}.pdf"
    return FileResponse(io.BytesIO(pdf_bytes), as_attachment=True, filename=filename)


def health(request: HttpRequest) -> HttpResponse:
    return HttpResponse("ok")
