from django.contrib import admin
from django.urls import include, path

from .utilities import github_webhook

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("app_studyhub.urls")),
    path("webhook-update/", view=github_webhook, name="github-webhook-view"),
]


# Override some AdminSite attributes to customize default text in Admin site
admin.AdminSite.empty_value_display = "---"
admin.AdminSite.site_header = "StudyHub"
admin.AdminSite.site_title = "StudyHub"
admin.AdminSite.index_title = "Administration"
