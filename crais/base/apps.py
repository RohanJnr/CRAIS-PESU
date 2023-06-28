from django.apps import AppConfig


class BaseConfig(AppConfig):
    """Django AppConfig for base app."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'crais.base'
