from django.apps import AppConfig

class ApiConfig(AppConfig):
    name = 'api'

    def ready(self):
        import stripe
        from django.conf import settings
        stripe.api_key = settings.STRIPE_SECRET_KEY