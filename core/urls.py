from django.contrib import admin
from django.http import JsonResponse
from django.urls import path

from prisederef.tasks import ping
from core.views import home, login_view, logout_view
from prisederef.views import recruiter_home, submit_reference, invite_landing, references_view, reference_detail_view


def health(_request):
    ping.delay()
    return JsonResponse({"status": "ok"})


urlpatterns = [
    path("", home, name="home"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("admin/", admin.site.urls),
    path("health/", health),
    path("candidates/", recruiter_home, name="candidates"),
    path("references/", references_view, name="references"),
    path("references/<int:reference_id>/", reference_detail_view, name="reference_detail"),
    path("references/<uuid:token>/", invite_landing, name="invite_landing"),
    path("references/<uuid:token>/submit/", submit_reference, name="submit_reference"),
]
