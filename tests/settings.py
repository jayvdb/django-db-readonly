SECRET_KEY = "notsecr3t"

DB_READ_ONLY_MIDDLEWARE_MESSAGE = False
SITE_READ_ONLY = False
DB_READ_ONLY_DATABASES = []

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    },
}

INSTALLED_APPS = [
    "readonly",
    "tests",
]

MIDDLEWARE = [
    "readonly.middleware.DatabaseReadOnlyMiddleware",
]
