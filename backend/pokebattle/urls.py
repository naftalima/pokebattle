from django.conf.urls import include, url  # noqa
from django.contrib import admin
from django.urls import path

import django_js_reverse.views


urlpatterns = [
    path("admin/", admin.site.urls, name="admin"),
    path("jsreverse/", django_js_reverse.views.urls_js, name="js_reverse"),
    path("", include("battles.urls")),
    path("", include("battles.urls")),
    path("", include("users.urls")),
    path("api/", include(("battles.api.urls", "api"), namespace="api")),
]
