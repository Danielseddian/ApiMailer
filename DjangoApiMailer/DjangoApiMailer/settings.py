from pathlib import Path
from os import path, getenv
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

if path.exists(env_path := path.join(BASE_DIR, ".env")):
    load_dotenv(env_path)

context_processors = "django.template.context_processors."
contrib = "django.contrib."
middleware = "django.middleware."
password_validation = contrib + "auth.password_validation."

DJANGO_APPS = [
    contrib + "admin",
    contrib + "auth",
    contrib + "contenttypes",
    contrib + "sessions",
    contrib + "messages",
    contrib + "staticfiles",
    "django_filters",
    "corsheaders",
    "rest_framework",
    "rest_framework.authtoken",
]

LOCAL_APPS = [
    "ApiMailer.apps.ApimailerConfig",
]

OTHER_APPS = [
    "djoser",
    "django_celery_beat",
    "django_celery_results",
]

INSTALLED_APPS = DJANGO_APPS + LOCAL_APPS + OTHER_APPS

MIDDLEWARE = [
    middleware + "security.SecurityMiddleware",
    contrib + "sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    middleware + "common.CommonMiddleware",
    middleware + "csrf.CsrfViewMiddleware",
    contrib + "auth.middleware.AuthenticationMiddleware",
    contrib + "messages.middleware.MessageMiddleware",
    middleware + "clickjacking.XFrameOptionsMiddleware",
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                context_processors + "debug",
                context_processors + "request",
                contrib + "auth.context_processors.auth",
                contrib + "messages.context_processors.messages",
            ],
        },
    },
]

DATABASES = {
    "default": {
        "ENGINE": getenv("DB_ENGINE", "django.db.backends.sqlite3"),
        "NAME": getenv("DB_NAME", "db.sqlite3"),
        "USER": getenv("POSTGRES_USER", "postgres"),
        "PASSWORD": getenv("POSTGRES_PASSWORD", "postgres"),
        "HOST": getenv("DB_HOST", "localhost"),
        "PORT": getenv("DB_PORT", "5432"),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": password_validation + "UserAttributeSimilarityValidator",
    },
    {
        "NAME": password_validation + "MinimumLengthValidator",
    },
    {
        "NAME": password_validation + "CommonPasswordValidator",
    },
    {
        "NAME": password_validation + "NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "ru-ru"

TIME_ZONE = "Europe/Moscow"

USE_I18N = True

USE_L10N = True

USE_TZ = True

CORS_ORIGIN_ALLOW_ALL = True

CORS_URLS_REGEX = r"^/api/.*$"

STATIC_ROOT = path.join(BASE_DIR, "back_static")

STATIC_URL = "/back_static/"

MEDIA_ROOT = path.join(BASE_DIR, "media")

MEDIA_URL = "/media/"

SECRET_KEY = getenv("SECRET_KEY", "some_secret_key")

DEBUG = getenv("DEBUG", True)

ALLOWED_HOSTS = getenv("ALLOWED_HOSTS", "localhost web 127.0.0.1").split()

ROOT_URLCONF = "DjangoApiMailer.urls"

WSGI_APPLICATION = "DjangoApiMailer.wsgi.application"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Celery Configuration Options
CELERY_TIMEZONE = "Europe/Moscow"

CELERY_TASK_TRACK_STARTED = True

CELERY_TASK_TIME_LIMIT = 30 * 60

CELERY_BROKER_URL = "redis://localhost:6379/0"

CELERY_RESULT_BACKEND = "django-db"

MAILING_TOKEN = getenv("MAILING_TOKEN")

MAILING_URL = "https://probe.fbrq.cloud/v1/send"
