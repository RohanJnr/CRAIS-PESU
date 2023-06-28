from django.db import models
from wagtail.admin.panels import FieldPanel

from .form_page import FormPage


class ContactPage(FormPage):
    contact_email = models.CharField(max_length=255)
    contact_phone = models.CharField(max_length=12, null=True, blank=True, help_text="This is optional.")
    contact_address = models.TextField()

    parent_page_types = ("base.HomePage",)


    content_panels = FormPage.content_panels + [
        FieldPanel('contact_email'),
        FieldPanel('contact_phone'),
        FieldPanel('contact_address')
    ]