from django.apps import AppConfig


class YourAppNameConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'your_app_name'

    def ready(self):
        import your_app_name.signals  # noqa


class RankdarbiaiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Rankdarbiai'
