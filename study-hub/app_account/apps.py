from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AppAccountConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "app_account"
    verbose_name = _("Account")
    verbose_name_plural = _("Accounts")
