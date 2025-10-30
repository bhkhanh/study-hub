import uuid
from pathlib import Path

from autoslug import AutoSlugField
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

# get the current user model instead of importing directly
current_user_model = get_user_model()


def cover_image_upload_to(instance, filename) -> str:
    """Generate file path and file name for cover images."""

    filepath = Path(filename)
    file_extension = filepath.suffix.lower()
    obj_id = instance.id
    class_name = instance.__class__.__name__.lower()
    upload_to = f"images/{class_name}-covers/{obj_id}_cover{file_extension}"
    return upload_to


class BaseAppModel(models.Model):
    """
    The purpose of this Abstract base model is to stop repeating/duplicating code
    with common fields in some models.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(unique=True, max_length=255)
    slug_name = AutoSlugField(
        populate_from="name",
        unique=True,
        always_update=True,
        editable=True,
    )
    is_active = models.BooleanField(default=True)
    description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(
        to=current_user_model,
        on_delete=models.PROTECT,
        related_name="%(class)s_creators",
        editable=False,
    )
    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    modified_by = models.ForeignKey(
        to=current_user_model,
        on_delete=models.PROTECT,
        related_name="%(class)s_modifiers",
        blank=True,
        null=True,
    )
    last_modified = models.DateTimeField(blank=True, null=True)
    cover_image = models.FileField(
        upload_to=cover_image_upload_to,
        max_length=255,
        blank=True,
        null=True,
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.name or self.pk


class Category(BaseAppModel):
    """
    Category model is for organizing or grouping subcategories (subjects).
    """

    class Meta:
        db_table = "studyhub_category"
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        ordering = ["-is_active", "name"]

    def get_absolute_url(self):
        return reverse(
            viewname="category-detail-view",
            kwargs={"slug_name": self.slug_name},
        )


class Subcategory(BaseAppModel):
    """
    Subcategory (Subject) model is the smaller group of Category model,
    (e.g. Subjects/Courses of a specific Department).
    """

    category = models.ForeignKey(
        to=Category,
        on_delete=models.PROTECT,
        related_name="subcategories",
    )

    class Meta:
        db_table = "studyhub_subcategory"
        verbose_name = _("Subject")
        verbose_name_plural = _("Subjects")
        ordering = ["-is_active", "name"]

    def get_absolute_url(self):
        return reverse(
            viewname="subcategory-detail-view",
            kwargs={
                "category_slugname": self.category.slug_name,
                "subcategory_slugname": self.slug_name,
            },
        )


class File(BaseAppModel):
    """
    File model contains information of uploaded files/documents (PDF, docx, pptx, ...)
    """

    class FileType(models.TextChoices):
        LESSON = "lesson", _("Lesson")
        EXERCISE = "exercise", _("Exercise")
        BOOK = "book", _("Book")
        PRACTICE = "practice", _("Practice")

    class FileLanguage(models.TextChoices):
        ENGLISH = "en", _("English")
        VIETNAMESE = "vi", _("Vietnamese")

    def file_upload_to(instance, filename) -> str:
        """Generate file path and file name as the destination for uploaded files."""
        filepath = Path(filename)
        file_extension = filepath.suffix.lower()
        obj_category = instance.subcategory.category.slug_name
        obj_subcategory = instance.subcategory.slug_name
        obj_filetype = instance.file_type
        obj_name = instance.slug_name
        upload_to = f"files/{obj_category}/{obj_subcategory}/{obj_filetype}__{obj_name}{file_extension}"
        return upload_to

    is_active = None  # don't use this field
    description = None  # don't use this field
    cover_image = None  # don't use this field

    subcategory = models.ForeignKey(
        to=Subcategory,
        on_delete=models.PROTECT,
        related_name="files",
    )
    file_type = models.CharField(
        max_length=20,
        choices=FileType,
        default=FileType.LESSON,
    )
    file_language = models.CharField(
        max_length=20,
        choices=FileLanguage,
        default=FileLanguage.ENGLISH,
    )
    uploaded_file = models.FileField(upload_to=file_upload_to, max_length=255)

    class Meta:
        db_table = "studyhub_file"
        verbose_name = _("File")
        verbose_name_plural = _("Files")
        ordering = ["-last_modified", "-date_created"]
