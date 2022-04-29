from django.apps import AppConfig


class NonDataProviderConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'non_data_provider'
