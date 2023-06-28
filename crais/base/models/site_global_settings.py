from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting
from wagtail.fields import RichTextField


@register_setting
class SiteGlobalSettings(BaseSiteSetting):
    """Global settings for navbar and footer."""

    navbar_announcement = RichTextField(
        help_text="Single line text, creating a hyperlink will style it as a button.",
        blank=True,
        null=True
    )
    footer_text = models.CharField(max_length=255, blank=True, null=True)

    logo_combined = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    crais_logo = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    pesu_logo = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    favicon = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    panels = [
        FieldPanel("navbar_announcement"),
        FieldPanel("footer_text"),
        FieldPanel("logo_combined"),
        FieldPanel("crais_logo"),
        FieldPanel("pesu_logo"),
        FieldPanel("favicon")
    ]
