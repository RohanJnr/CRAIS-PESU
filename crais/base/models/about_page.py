from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField
from wagtail.models import Page


class AboutPage(Page):
    """Model for about page."""

    parent_page_types = ("base.HomePage",)

    title_part_1 = models.CharField(max_length=64)
    title_part_2 = models.CharField(max_length=64)
    landing_page_paragraph = models.CharField(max_length=312)

    body = RichTextField()

    content_panels = Page.content_panels + [
        FieldPanel("title_part_1"),
        FieldPanel("title_part_2"),
        FieldPanel("landing_page_paragraph"),
        FieldPanel("body")
    ]

    max_count = 1
