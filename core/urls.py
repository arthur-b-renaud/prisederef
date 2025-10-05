from django.contrib import admin
from django.http import JsonResponse
from django.urls import path

from prisederef.tasks import ping
from core.views import home


def health(_request):
    ping.delay()
    return JsonResponse({"status": "ok"})


urlpatterns = [
    path("", home, name="home"),
    path("admin/", admin.site.urls),
    path("health/", health),
]
