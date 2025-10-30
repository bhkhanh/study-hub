import uuid
from pathlib import Path

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _


class UserAccount(AbstractUser):
    """UserAccount model which is extended from AbstractUser class model."""

    first_name = None  # not use this field in this model
    last_name = None  # not use this field in this model

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(_("e-mail address"), unique=True)

    class Meta:
        db_table = "account_user"
        verbose_name = "User"
        verbose_name_plural = "Users"

    def get_full_name(self):
        """Return the full name or username of the user."""
        try:
            return self.user_profile.full_name
        except (UserProfile.DoesNotExist, AttributeError):
            return self.username

    def get_short_name(self):
        """
        Return the full name or empty string
        because of not using first_name and last_name fields.
        """
        try:
            return self.user_profile.full_name
        except (UserProfile.DoesNotExist, AttributeError):
            return ""

    def __str__(self):
        return self.username or self.id


class UserProfile(models.Model):
    """UserProfile model for each of the UserAccount been created."""

    class UserGender(models.TextChoices):
        """User gender choice options."""

        MALE = "male", "Male"
        FEMALE = "female", "Female"
        OTHER = "other", "Other"

    def profile_image_upload_to(instance, filename) -> str:
        """Generate file path and file name for user profile images."""

        filepath = Path(filename)
        file_extension = filepath.suffix.lower()
        user_id = instance.user_account.id
        upload_to = f"images/user-avatars/{user_id}_avatar{file_extension}"
        return upload_to

    full_name = models.CharField(max_length=255, blank=False, null=True)
    birthdate = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=8, choices=UserGender, default=UserGender.MALE)
    user_account = models.OneToOneField(
        to=UserAccount,
        on_delete=models.CASCADE,
        related_name="user_profile",
        primary_key=True,
        editable=False,
    )
    avatar = models.ImageField(
        upload_to=profile_image_upload_to,
        max_length=150,
        blank=True,
        null=True,
    )

    class Meta:
        db_table = "account_user_profile"
        verbose_name = "user profile"
        verbose_name_plural = "user profiles"

    def __str__(self):
        return self.full_name or self.user_account.username


@receiver(signal=post_save, sender=UserAccount)
def create_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile(user_account=instance).save()


class Feedback(models.Model):
    class ProcessStatus(models.TextChoices):
        NOT_STARTED = "not-started", "Not started"
        IN_PROGRESS = "in-progress", "In progress"
        COMPLETED = "completed", "Completed"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(max_length=200)
    email = models.EmailField(_("e-mail address"))
    phone = models.CharField(max_length=20, blank=True, null=True)
    message = models.TextField(blank=False, null=False)
    sent_at = models.DateTimeField(auto_now_add=True, editable=False)
    response_from_us = models.TextField(blank=True, null=True)
    process_status = models.CharField(
        max_length=15,
        choices=ProcessStatus,
        default=ProcessStatus.NOT_STARTED,
    )

    class Meta:
        db_table = "account_feedback_message"
        verbose_name = _("Feedback message")
        verbose_name_plural = _("Feedback messages")
        ordering = ["-sent_at"]
