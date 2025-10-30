from django.contrib import admin
from django.utils import timezone
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from .models import Category, File, Subcategory


class BaseAppModelAdmin(admin.ModelAdmin):
    """"""

    list_display = [
        "name",
        "cover_image",
        "date_created",
        "created_by",
        "last_modified",
        "modified_by",
        "is_active",
    ]
    readonly_fields = ["created_by", "date_created", "modified_by", "last_modified"]
    fieldsets = (
        (
            _("Basic information"),
            {"fields": ("name", "description", "cover_image", "is_active")},
        ),
        (
            _("Detail information"),
            {"fields": ("created_by", "date_created", "modified_by", "last_modified")},
        ),
    )
    ordering = ["-is_active", "name"]

    def get_fieldsets(self, request, obj):
        add_fieldsets = (
            (
                _("Basic information"),
                {"fields": ("name", "description", "cover_image")},
            ),
        )
        if not obj:
            return add_fieldsets
        return super().get_fieldsets(request, obj)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields["name"].label = _("Name")
        form.base_fields["name"].help_text = _(
            "Required. The name that will be visible to users."
        )
        form.base_fields["description"].label = _("Description")
        form.base_fields["description"].help_text = _(
            "(Optional) Brief description or note for this item."
        )
        form.base_fields["cover_image"].label = _("Cover picture")
        form.base_fields["cover_image"].help_text = _(
            "(Optional) Upload a cover image as representative picture of this item and it is visible to users."
        )
        if obj:
            form.base_fields["is_active"].label = "Active"
            form.base_fields["is_active"].help_text = (
                "Designates whether this item is visible and can be accessible to users.\
                Instead of deleting this item, just unchecked this option."
            )
        return form

    def save_form(self, request, form, change):
        instance = form.save(commit=False)
        if not change:
            instance.created_by = request.user
        else:
            instance.modified_by = request.user
            instance.last_modified = timezone.now()
        return instance


class FileInline(admin.TabularInline):
    """Admin display stacked inline of File model."""

    model = File
    extra = 0
    classes = ["collapse"]
    ordering = ["name"]
    fields = ["name", "uploaded_file", "file_type", "file_language"]
    readonly_fields = ["date_created", "created_by", "last_modified", "modified_by"]


class SubcategoryInline(admin.TabularInline):
    """Admin display stacked inline of Subcategory model."""

    model = Subcategory
    extra = 0
    readonly_fields = ["date_created", "created_by", "last_modified", "modified_by"]

    def get_fieldsets(self, request, obj):
        add_fieldsets = (
            (
                None,
                {
                    "fields": (
                        "name",
                        "description",
                        "cover_image",
                    ),
                },
            ),
        )
        fieldsets = (
            (
                None,
                {
                    "fields": (
                        "name",
                        "description",
                        "cover_image",
                        "is_active",
                    ),
                },
            ),
            (
                "Activities",
                {
                    "fields": (
                        "date_created",
                        "created_by",
                        "last_modified",
                        "modified_by",
                    ),
                },
            ),
        )

        if not obj:
            return add_fieldsets
        return fieldsets


@admin.register(Category)
class CategoryAdmin(BaseAppModelAdmin):
    """Admin display of Category model."""

    # inlines = [SubcategoryInline]

    # def get_inline_instances(self, request, obj):
    #     return (
    #         obj and super(CategoryAdmin, self).get_inline_instances(request, obj) or []
    #     )

    # def save_formset(self, request, form, formset, change):
    #     instances = formset.save(commit=False)

    #     for each_instance in instances:
    #         each_instance.uploaded_by = request.user

    #         if change:
    #             each_instance.last_modified = timezone.now()

    #         each_instance.save()

    #     formset.save_m2m()


@admin.register(Subcategory)
class SubcategoryAdmin(BaseAppModelAdmin):
    """Admin display of Subcategory model."""

    # inlines = [FileInline]
    list_display = [
        "name",
        "category",
        "cover_image",
        "date_created",
        "created_by",
        "last_modified",
        "modified_by",
        "is_active",
    ]
    fieldsets = (
        (
            _("Basic information"),
            {"fields": ("name", "category", "description", "cover_image", "is_active")},
        ),
        (
            _("Detail information"),
            {"fields": ("created_by", "date_created", "modified_by", "last_modified")},
        ),
    )

    def get_fieldsets(self, request, obj):
        add_fieldsets = (
            (
                _("Basic information"),
                {"fields": ("name", "category", "description", "cover_image")},
            ),
        )
        if not obj:
            return add_fieldsets
        return super().get_fieldsets(request, obj)

    # def get_inline_instances(self, request, obj):
    #     return (
    #         obj
    #         and super(SubcategoryAdmin, self).get_inline_instances(request, obj)
    #         or []
    #     )

    # def save_formset(self, request, form, formset, change):
    #     """Handle saving the inline objects/fields."""
    #     instances = formset.save(commit=False)
    #     for each_instance in instances:
    #         if not each_instance._state.adding:
    #             each_instance.modified_by = request.user
    #             each_instance.last_modified = timezone.now()
    #         else:
    #             each_instance.created_by = request.user
    #         each_instance.save()
    #     for each_deleted_instance in formset.deleted_objects:
    #         each_deleted_instance.delete()
    #     formset.save_m2m()

    # def get_inline_formsets(self, request, formsets, inline_instances, obj):
    #     inline_formsets_class = super().get_inline_formsets(
    #         request, formsets, inline_instances, obj
    #     )
    #     for each in inline_formsets_class:
    #         print(each)


@admin.register(File)
class FileAdmin(BaseAppModelAdmin):
    """Admin display of File model."""

    list_display = [
        "name",
        "display_custom_subcategory",
        "display_custom_uploaded_file",
        "display_custom_file_type",
        "display_custom_file_language",
        "display_custom_date_created",
        "display_custom_last_modified",
    ]
    ordering = ["-date_created", "-last_modified", "name"]
    fieldsets = (
        (
            _("Basic information"),
            {
                "fields": (
                    "name",
                    "subcategory",
                    "uploaded_file",
                    "file_type",
                    "file_language",
                )
            },
        ),
        (
            _("Detail information"),
            {"fields": ("created_by", "date_created", "modified_by", "last_modified")},
        ),
    )

    def get_fieldsets(self, request, obj):
        add_fieldsets = (
            (
                _("Basic information"),
                {
                    "fields": (
                        "name",
                        "subcategory",
                        "file_type",
                        "file_language",
                        "uploaded_file",
                    )
                },
            ),
        )
        if not obj:
            return add_fieldsets
        return super().get_fieldsets(request, obj)

    def get_form(self, request, obj=None, **kwargs):
        form = admin.ModelAdmin.get_form(self, request, obj, **kwargs)
        form.base_fields["name"].label = _("Name")
        form.base_fields["name"].help_text = _(
            "Required. The name that will be visible to users."
        )
        form.base_fields["subcategory"].label = _("Subject")
        form.base_fields["subcategory"].help_text = _(
            "Required. Choose subject that this file item will belong to."
        )
        form.base_fields["file_type"].help_text = _("What is the kind of this file?")
        form.base_fields["file_language"].help_text = _(
            "What is the language of this file?"
        )
        form.base_fields["uploaded_file"].label = _("File")
        return form

    @admin.display(description=_("Subject"))
    def display_custom_subcategory(self, obj):
        return obj.subcategory.name

    @admin.display(description=_("File"))
    def display_custom_uploaded_file(self, obj):
        if obj.uploaded_file:
            return format_html(
                "<a target=_blank href={}>{}</a>",
                obj.uploaded_file.url,
                obj.uploaded_file.name,
            )
        return obj.uploaded_file

    @admin.display(description=_("Type"))
    def display_custom_file_type(self, obj):
        return obj.get_file_type_display()

    @admin.display(description=_("Language"))
    def display_custom_file_language(self, obj):
        return obj.get_file_language_display()

    @admin.display(description=_("Date created"), ordering="date_created")
    def display_custom_date_created(self, obj):
        if obj.date_created:
            return obj.date_created.strftime("%d/%m/%Y, %I:%M %p")
        return obj.date_created

    @admin.display(description=_("Last modified"), ordering="last_modified")
    def display_custom_last_modified(self, obj):
        if obj.last_modified:
            return obj.last_modified.strftime("%d/%m/%Y, %I:%M %p")
        return obj.last_modified
