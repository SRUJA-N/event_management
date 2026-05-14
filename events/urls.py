from django.urls import path

from . import views

app_name = "events"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("health/", views.health, name="health"),
    path("events/", views.event_list, name="event_list"),
    path("events/create/", views.event_create, name="event_create"),
    path("events/<int:pk>/", views.event_detail, name="event_detail"),
    path("events/<int:pk>/edit/", views.event_edit, name="event_edit"),
    path("events/<int:pk>/qr.png", views.event_qr, name="event_qr"),
    path("events/<int:pk>/certificate/<str:usn>/", views.certificate_pdf, name="certificate"),
    path("predictor/", views.predictor_view, name="predictor"),
    path("scan/<int:event_id>/", views.scan_public, name="scan_public"),
]
