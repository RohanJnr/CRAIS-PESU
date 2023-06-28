from django.apps import AppConfig
from django.db.models.signals import post_save


class ContentConfig(AppConfig):
    """Django AppConfig for content app."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'crais.content'

    def ready(self) -> None:
        """Connect create_event_registration_form signal to EventPage model."""
        from .signals import create_event_registration_form

        event_page_model = self.get_model("EventPage")
        post_save.connect(create_event_registration_form, sender=event_page_model)
