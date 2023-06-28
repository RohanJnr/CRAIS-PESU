from django.db import models
from django.http import HttpRequest
from wagtail.admin.panels import FieldPanel
from wagtail.models import Page


class EventIndexPage(Page):
    """Page to list all events."""

    intro = models.CharField(max_length=256)

    content_panels = Page.content_panels + [FieldPanel("intro", classname="full")]

    parent_page_types = ("base.HomePage",)
    subpage_types = ("content.EventPage",)
    max_count = 1

    def get_context(self, request: HttpRequest, *args, **kwargs) -> dict:
        """Update context to include only published posts, ordered by reverse-chron."""
        context = super().get_context(request)

        events = self.get_children().live().order_by("-timestamp")

        context["events"] = events
        return context
