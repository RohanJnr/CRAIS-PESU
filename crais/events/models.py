from django.db import models
from django import forms
from django.http import HttpRequest
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey
from taggit.models import TaggedItemBase
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.fields import RichTextField
from wagtail.models import Page, Orderable
from wagtail.search import index
from wagtail.snippets.models import register_snippet


EVENT_STATUS_CHOICES = (
    ("Completed", "COMPLETED"),
    ("Upcoming", "UPCOMING")
)



class EventIndexPage(Page):
    intro = models.CharField(max_length=255)

    content_panels = Page.content_panels + [FieldPanel("intro")]

    parent_page_types = ("base.HomePage",)
    subpage_types = ("events.EventPage",)
    max_count = 1

    def get_context(self, request: HttpRequest, *args, **kwargs) -> dict:
        """Update context to include only published posts, ordered by reverse-chron."""
        context = super().get_context(request)

        eventpages = self.get_children().live().order_by("-first_published_at")

        context["eventpages"] = eventpages
        return context


class EventPage(Page):
    intro = models.CharField(max_length=255)
    description = RichTextField()
    banner = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    date = models.DateField(blank=True, null=True)

    status = models.CharField(max_length=32, choices=EVENT_STATUS_CHOICES)

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
        FieldPanel("description"),
        FieldPanel("banner"),
        FieldPanel("date"),
        FieldPanel("status"),
    ]

    parent_page_types = ("events.EventIndexPage",)
    subpage_types = ("base.FormPage", )