from django.apps import AppConfig
from django.db.models.signals import post_save


class EventsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'crais.events'

    def ready(self):
        from .signals import create_event_registration_form

        EventPage: type = self.get_model("EventPage")
        # post_save.connect(create_event_registration_form, sender=EventPage)
