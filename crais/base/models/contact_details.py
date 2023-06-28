from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting


@register_setting
class ContactGlobalSettings(BaseSiteSetting):
    """Contact details of CRAIS."""

    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=12, null=True, blank=True, help_text="This is optional.")
    address = models.TextField()

    address_link = models.URLField(help_text="Link to directions on google maps or similar platforms.")


    parent_page_types = ("base.HomePage",)


    panels = [
        FieldPanel('email'),
        FieldPanel('phone'),
        FieldPanel('address')
    ]
