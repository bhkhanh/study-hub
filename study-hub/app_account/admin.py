from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import Feedback, UserAccount, UserProfile


class UserProfileInline(admin.StackedInline):
    """Admin display stacked inline of UserProfile model."""

    model = UserProfile
    extra = 0
    can_delete = False
    min_num = 1
    max_num = 1
    show_full_result_count = False
    verbose_name = "personal information"

    def get_fieldsets(self, request, obj):
        fieldsets = (
            (
                None,
                {
                    "fields": (
                        "full_name",
                        "birthdate",
                        "gender",
                        "avatar",
                    ),
                },
            ),
        )
        add_fieldsets = (
            (
                None,
                {
                    "fields": (
                        "full_name",
                        "birthdate",
                        "gender",
                        "avatar",
                    ),
                },
            ),
        )

        if not obj:
            return add_fieldsets
        return fieldsets

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        formset.form.base_fields["full_name"].help_text = (
            "Required. Enter your full name or your custom display name are also allowed."
        )
        formset.form.base_fields["gender"].help_text = (
            "Required. Choose your gender (default is Male)."
        )
        formset.form.base_fields["birthdate"].label = "Date of birth"
        formset.form.base_fields["birthdate"].help_text = (
            "Required. What is your birthday? Tell us."
        )
        formset.form.base_fields["avatar"].label = "Profile image"
        formset.form.base_fields["avatar"].help_text = (
            "(Optional) Upload your profile picture if you want to."
        )
        return formset


@admin.register(UserAccount)
class UserAccountAdmin(UserAdmin):
    """
    Admin display of UserAccount model
    and it is extended from UserAdmin class.
    """

    list_filter = []
    search_fields = []
    inlines = [UserProfileInline]
    readonly_fields = ["display_last_login", "display_date_joined"]
    ordering = ["-is_active", "username"]
    list_display = [
        "username",
        "email",
        "display_user_fullname",
        "display_user_gender",
        "display_user_birthdate",
        "display_last_login",
        "is_staff",
        "is_superuser",
        "is_active",
    ]
    add_fieldsets = (
        (
            _("Account information"),
            {
                "fields": (
                    "username",
                    "email",
                    "password1",
                    "password2",
                ),
            },
        ),
        (
            _("Account permissions"),
            {
                "classes": ("collapse",),
                "fields": (
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
    )
    fieldsets = (
        (
            _("Account information"),
            {
                "fields": (
                    "username",
                    "email",
                    "password",
                    "display_date_joined",
                    "display_last_login",
                ),
            },
        ),
        (
            _("Account permissions"),
            {
                "classes": ("collapse",),
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields["email"].help_text = (
            "Required. Enter a valid E-mail address (e.g. example@gmail.com), "
            "for authentication, password recovery,..."
        )

        return form

    @admin.display(description=_("Name"))
    def display_user_fullname(self, obj):
        return obj.user_profile.full_name

    @admin.display(description=_("Gender"))
    def display_user_gender(self, obj):
        return obj.user_profile.get_gender_display()

    @admin.display(description=_("Day of birth"))
    def display_user_birthdate(self, obj):
        if obj.user_profile.birthdate:
            return obj.user_profile.birthdate.strftime("%d/%m/%Y")
        return obj.user_profile.birthdate

    @admin.display(description=_("Last login"))
    def display_last_login(self, obj):
        if obj.last_login:
            custom_last_login = obj.last_login
            return custom_last_login.strftime("%d/%m/%Y, %I:%M %p")
        else:
            return obj.last_login

    @admin.display(description=_("Date joined"))
    def display_date_joined(self, obj):
        if obj.date_joined:
            custom_date_joined = obj.date_joined
            return custom_date_joined.strftime("%d/%m/%Y, %I:%M %p")
        else:
            return obj.date_joined


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = [
        "email",
        "full_name",
        "phone",
        "message",
        "sent_at",
        "response_from_us",
        "process_status",
    ]
    readonly_fields = ["email", "full_name", "phone", "message", "sent_at"]

    def has_add_permission(self, request):
        return False
