from atexit import register
from crais.base.models import FormPage, FormField


def create_event_registration_form(sender: type, instance, *args, **kwargs):
    if not instance.get_children():
        registration_form_page = FormPage(
            title=f"Register for {instance.title}",
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