import os
import json
from pathlib import Path
from corsheaders.defaults import default_headers

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = BASE_DIR.parent

MIGRATE_PROD = os.getenv("MIGRATE_PROD", "FALSE").upper() == "TRUE"
GIT_VERSION = os.getenv("KAMAL_VERSION", "NONE")

CONFIG_PATH = "/etc/_KAHN_PROJECT_SLUG_.json"
with open(CONFIG_PATH) as f:
    CONFIG = json.loads(f.read())
    print(f"Loaded config from {CONFIG_PATH}")

SECRET_KEY = CONFIG["SECRET_KEY"]

DEBUG = CONFIG["DEBUG"]
print("DEBUG:", DEBUG, type(DEBUG))

NGROK = False

if DEBUG:
    if NGROK:
        HOST = "4e8000.ngrok.io"
        FRONTEND_HOST = "4e3000.ngrok.io"
        FRONTEND_URL = f"https://{FRONTEND_HOST}"
        ALLOWED_HOSTS = [HOST]
        CORS_ALLOWED_ORIGINS = [FRONTEND_URL]

        CSRF_COOKIE_SECURE = True
        CSRF_COOKIE_SAMESITE = "None"
        CSRF_COOKIE_HTTPONLY = False
        CSRF_COOKIE_DOMAIN = HOST
        CSRF_TRUSTED_ORIGINS = [FRONTEND_URL]

        SESSION_COOKIE_DOMAIN = HOST
        SESSION_COOKIE_SECURE = True
        SESSION_COOKIE_SAMESITE = "None"
    else:
        HOST = "localhost:8000"
        FRONTEND_HOST = "localhost:3000"
        FRONTEND_URL = f"http://{FRONTEND_HOST}"
        ALLOWED_HOSTS = ["localhost"]
        CORS_ALLOWED_ORIGINS = [FRONTEND_URL]
        CSRF_TRUSTED_ORIGINS = [FRONTEND_URL]
else:
    HOST = CONFIG["HOST"]
    FRONTEND_HOST = f"todo.argonrec.com"
    FRONTEND_URL = f"https://{FRONTEND_HOST}"
    ALLOWED_HOSTS = [HOST]
    CORS_ALLOWED_ORIGINS = [FRONTEND_URL]

    CSRF_COOKIE_SECURE = True
    CSRF_COOKIE_SAMESITE = "None"
    CSRF_COOKIE_HTTPONLY = False
    CSRF_COOKIE_DOMAIN = FRONTEND_HOST
    CSRF_TRUSTED_ORIGINS = [FRONTEND_URL]

    SESSION_COOKIE_DOMAIN = FRONTEND_HOST
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_SAMESITE = "None"

CORS_ALLOW_HEADERS = (
    *default_headers,
    "x-session-token",
    "x-email-verification-key",
    "x-password-reset-key",
)
CORS_ALLOW_CREDENTIALS = True

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "allauth",
    "allauth.account",
    "allauth.headless",
    # 'allauth.mfa',
    "corsheaders",
    "rest_framework",
    "rest_framework.authtoken",
    "core",
]

MIDDLEWARE = [
    "core.middleware.HealthCheckMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
]

ROOT_URLCONF = "_KAHN_PROJECT_SLUG_.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "templates",
            BASE_DIR / "templates/allauth",
        ],
        "APP_DIRS": False,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "_KAHN_PROJECT_SLUG_.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

if MIGRATE_PROD:
    MIGRATION_MODULES = {
        "core": "core.prod_migrations",
    }
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "prod_dummy.sqlite3",
        }
    }
elif DEBUG:
    MIGRATION_MODULES = {
        "core": "core.migrations",
    }
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / f"db.sqlite3",
        }
    }
else:
    MIGRATION_MODULES = {
        "core": "core.prod_migrations",
    }
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql_psycopg2",
            "NAME": CONFIG["DB_NAME"],
            "USER": CONFIG["DB_USER"],
            "PASSWORD": CONFIG["DB_PASS"],
            "HOST": CONFIG["DB_HOST"],
            "PORT": CONFIG["DB_PORT"],
        }
    }
print("MIGRATION MODULES:", MIGRATION_MODULES)


AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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

# AllAuth
HEADLESS_ONLY = True
# HEADLESS_CLIENTS = ("app",)
HEADLESS_CLIENTS = ("app", "browser")
HEADLESS_FRONTEND_URLS = {
    "account_confirm_email": f"{FRONTEND_URL}/verify/{{key}}",
    "account_reset_password_from_key": f"{FRONTEND_URL}/reset/{{key}}",
    "account_signup": f"{FRONTEND_URL}/signup",
}
ACCOUNT_SIGNUP_FIELDS = ["email*", "password1*", "password2*"]
ACCOUNT_LOGIN_METHODS = ["email"]
ACCOUNT_LOGIN_ON_PASSWORD_RESET = True
ACCOUNT_ADAPTER = "core.custom_adapter.CustomAccountAdapter"
HEADLESS_ADAPTER = "core.custom_adapter.CustomHeadlessAdapter"


REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        # "allauth.headless.contrib.rest_framework.authentication.XSessionTokenAuthentication",
        # "rest_framework.authentication.TokenAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAdminUser"],
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
    "TEST_REQUEST_DEFAULT_FORMAT": "json",
}


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Storage
DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
AWS_S3_REGION_NAME = CONFIG["AWS_S3_REGION_NAME"]
AWS_S3_ENDPOINT_URL = CONFIG["AWS_S3_ENDPOINT_URL"]
AWS_ACCESS_KEY_ID = CONFIG["AWS_ACCESS_KEY_ID"]
AWS_SECRET_ACCESS_KEY = CONFIG["AWS_SECRET_ACCESS_KEY"]
AWS_STORAGE_BUCKET_NAME = CONFIG["AWS_STORAGE_BUCKET_NAME"]
AWS_S3_FILE_OVERWRITE = False

# EMAIL
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

EMAIL_HOST = CONFIG["EMAIL_HOST"]
EMAIL_PORT = CONFIG["EMAIL_PORT"]
EMAIL_CONN_TYPE = CONFIG["EMAIL_CONN_TYPE"]
EMAIL_HOST_USER = CONFIG["EMAIL_HOST_USER"]
EMAIL_HOST_PASSWORD = CONFIG["EMAIL_HOST_PASS"]
DEFAULT_FROM_EMAIL = CONFIG["DEFAULT_FROM_EMAIL"]

if EMAIL_CONN_TYPE == "SSL":
    EMAIL_USE_SSL = True
elif EMAIL_CONN_TYPE == "TLS":
    EMAIL_USE_TLS = True
else:
    assert False, f"Unhandled conn type: {EMAIL_CONN_TYPE}"

if not DEBUG:
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "verbose": {
                "format": "{levelname} {asctime} {module} {message}",
                "style": "{",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "verbose",
            },
        },
        "root": {
            "handlers": ["console"],
            "level": "WARNING",
        },
        "loggers": {
            "django.request": {
                "handlers": ["console"],
                "level": "ERROR",
                "propagate": False,
            },
            "django.server": {
                "handlers": ["console"],
                "level": "INFO",
                "propagate": False,
            },
        },
    }
