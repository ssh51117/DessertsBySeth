import os

# Provide test defaults so decouple doesn't require .env in CI
os.environ.setdefault('SECRET_KEY', 'test-secret-key-not-used-in-production')
os.environ.setdefault('STRIPE_WEBHOOK_SECRET', 'whsec_test_fake')
os.environ.setdefault('STRIPE_SECRET_KEY', 'sk_test_fake')
os.environ.setdefault('RESEND_SECRET_KEY', 're_test_fake')

from dessertsbyseth.settings import *  # noqa

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}
