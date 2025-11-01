import os
from pathlib import Path

import dj_database_url
import environ
from django.utils.translation import gettext_lazy as _

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Configure ENV in Django application
# See https://django-environ.readthedocs.io/en/stable/quickstart.html
app_env = environ.Env()

# Take environment variables from .env file
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = app_env.str("DJANGO_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = app_env.bool("DJANGO_DEBUG", default=False)

ALLOWED_HOSTS = app_env.list("DJANGO_ALLOWED_HOSTS", default=["localhost", "127.0.0.1"])


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "whitenoise.runserver_nostatic",
    "django.contrib.staticfiles",
    # third-party apps:
    "crispy_forms",
    "crispy_bootstrap5",
    "storages",
    # local apps:
    "app_account",
    "app_studyhub",
]

# Set Bootstrap5 as and allowed template pack
# and as the default template pack for the project.
# https://github.com/django-crispy-forms/crispy-bootstrap5?tab=readme-ov-file#usage
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            str(BASE_DIR / "templates"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "app_studyhub.context_processors.category_list",  # category list
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases


DATABASES = {
    "default": dj_database_url.config(
        env="DJANGO_DATABASE_URL",
        engine="django.db.backends.postgresql",
        conn_max_age=900,  # (900 seconds = 15 minutes)
        conn_health_checks=True,
        ssl_require=False,
    )
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGES = [
    ("vi", _("Vietnamese")),
    ("en-us", _("English")),
]

LANGUAGE_CODE = app_env.str("DJANGO_LANGUAGE_CODE", default="en-us")

TIME_ZONE = app_env.str("DJANGO_TIME_ZONE", default="UTC")

USE_I18N = True

USE_L10N = True

USE_TZ = True


# https://docs.djangoproject.com/en/5.2/ref/settings/#locale-paths
LOCALE_PATHS = [
    str(BASE_DIR / "locale"),
]


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
STATIC_URL = "static/"


# Media files (user-uploaded files)
# https://docs.djangoproject.com/en/5.2/topics/files/

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "media/"


# Storages settings
# https://docs.djangoproject.com/en/5.2/ref/settings/#storages

STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3.S3Storage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}


# AWS S3 settings

# AWS Authentication with IAM user
AWS_ACCESS_KEY_ID = app_env.str("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = app_env.str("AWS_SECRET_ACCESS_KEY")

# AWS S3 bucket information:
AWS_STORAGE_BUCKET_NAME = app_env.str("AWS_STORAGE_BUCKET_NAME")
AWS_S3_REGION_NAME = app_env.str("AWS_S3_REGION_NAME")
AWS_S3_FILE_OVERWRITE = False
AWS_QUERYSTRING_AUTH = False


# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Session
# https://docs.djangoproject.com/en/5.2/ref/settings/#sessions
SESSION_EXPIRE_AT_BROWSER_CLOSE = True


# disable default User model, use our custom User model instead
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-user-model
AUTH_USER_MODEL = "app_account.UserAccount"


# The URL or named URL pattern where requests are redirected after login
# https://docs.djangoproject.com/en/5.2/ref/settings/#login-redirect-url
LOGIN_REDIRECT_URL = "home-view"  # redirect to home page

# # The URL or named URL pattern where requests are redirected after logout
# https://docs.djangoproject.com/en/5.2/ref/settings/#logout-redirect-url
LOGOUT_REDIRECT_URL = "home-view"  # redirect to home page


# Security
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
CSRF_TRUSTED_ORIGINS = app_env.list(
    "DJANGO_CSRF_TRUSTED_ORIGINS",
    default=["http://localhost:80", "http://127.0.0.1:80"],
)
