from django.db import models
from django.http import HttpRequest
from django.utils import timezone
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey
from taggit.models import TaggedItemBase
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.fields import RichTextField
from wagtail.models import Orderable, Page
from wagtail.search import index


class EventImages(Orderable):
    """Between 1 and 5 images for the home page carousel."""

    page = ParentalKey("content.EventPage", related_name="Event_images")
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    panels = [FieldPanel("image")]


class EventTimelineNode(Orderable):

    page = ParentalKey("content.EventPage", related_name="timelinenode")
    node_name = models.CharField(
        max_length=255
    )
    node_description = models.TextField()
    datetime_begin = models.DateTimeField()
    datetime_end = models.DateTimeField(
        null=True, blank=True
    )

    panels = [
        FieldPanel("node_name"),
        FieldPanel("node_description"),
        FieldPanel("datetime_begin"),
        FieldPanel("datetime_end")
    ]

class EventTag(TaggedItemBase):
    content_object = ParentalKey('content.EventPage', on_delete=models.CASCADE, related_name='tagged_items')

class EventPage(Page):
    intro = models.CharField(max_length=255)
    body = RichTextField()
    timestamp = models.DateTimeField(verbose_name="Date and Time")
    location = models.CharField(max_length=255)
    banner = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    registration_form = models.BooleanField(default=False)
    external_link_display_text = models.CharField(max_length=255, blank=True, null=True)
    external_link = models.URLField(blank=True, null=True, help_text="This field takes more priority over registration form page.")
    tags = ClusterTaggableManager(through=EventTag, blank=True)
    featured = models.BooleanField(default=False)

    search_fields = Page.search_fields + [
        index.SearchField("intro"),
    ]

    content_panels = Page.content_panels + [
        FieldPanel("timestamp"),
        FieldPanel("location"),
        FieldPanel("intro"),
        FieldPanel("body", classname="full"),
        FieldPanel("banner"),
        FieldPanel("registration_form"),
        FieldPanel("external_link_display_text"),
        FieldPanel("external_link"),
        FieldPanel("featured"),
        # FieldPanel("tags"),
        MultiFieldPanel(
            [InlinePanel("timelinenode", label="timelinenode")],
            heading="Event Timeline",
        ),
    ]

    parent_page_types = ("content.EventIndexPage",)
    subpage_types = ("base.FormPage",)

    def __repr__(self) -> str:
        return self.title

    def is_upcoming(self) -> bool:
        print(self.timestamp, timezone.now())
        if self.timestamp > timezone.now():
            return True
        return False

    def get_context(self, request: HttpRequest, *args, **kwargs) -> dict:
        """Update context to include only published posts, ordered by reverse-chron."""
        context = super().get_context(request)
        register_page = self.get_children().live().first()
        context["register_page"] = register_page
        return context
