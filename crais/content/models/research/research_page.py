from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField
from wagtail.models import Page


class ResearchPage(Page):
    """Page to showcase CRAIS research topics."""

    intro = models.CharField(max_length=255)
    information = RichTextField()

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
        FieldPanel("information"),
    ]

    parent_page_types = ("base.HomePage",)
    max_count = 1
