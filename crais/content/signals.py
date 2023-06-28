from crais.base.models import FormPage, FormField
from .models import EventPage


def create_event_registration_form(_sender: type, instance: EventPage, *args, **kwargs) -> None:
    """Create a basic registration form automatically for events when required."""
    if instance.registration_form:
        if not instance.get_children():
            registration_form_page = FormPage(
                title=f"Register for {instance.title}",
                intro="This is intro",
                general_information="Information",
                thank_you_text="Thank you for registering! Event details will be sent a day prior to the event.",
                slug="register"
            )

            registration_form_page.form_fields = [
                FormField(label="Name", field_type="singleline"),
                FormField(label="Email", field_type="email")
            ]

            instance.add_child(instance=registration_form_page)

        else:
            register_page = instance.get_children().live().first()
            register_page.title = f"Register for {instance.title}"
            register_page.save()
