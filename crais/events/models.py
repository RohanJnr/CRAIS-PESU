from django.db import models
from django.http import HttpRequest
from django.utils import timezone
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


class EventTimelineNode(Orderable):

    page = ParentalKey("events.EventPage", related_name="timelineNode")
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

        event_timestamps = EventPage.objects.order_by().values('start_timestamp').distinct()
        context["event_timestamps"] = event_timestamps

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

    start_timestamp = models.DateTimeField(verbose_name="Event start date and time.")
    end_timestamp = models.DateTimeField(verbose_name="Event end date and time.")
    venue = models.CharField(max_length=255)
    featured = models.BooleanField(default=False)

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
        FieldPanel("description"),
        FieldPanel("banner"),
        FieldPanel("start_timestamp"),
        FieldPanel("end_timestamp"),
        FieldPanel("venue"),
        FieldPanel("featured"),
        MultiFieldPanel(
            [InlinePanel("timelineNode", label="timelineNode")],
            heading="Event Timeline",
        ),
    ]

    parent_page_types = ("events.EventIndexPage",)
    subpage_types = ("base.FormPage", )

    def get_context(self, request: HttpRequest, *args, **kwargs) -> dict:
        """Update context to include only published posts, ordered by reverse-chron."""
        context = super().get_context(request)
        register_page = self.get_children().live().first()
        context["register_page"] = register_page
        return context

    def get_status(self: "EventPage") -> str:
        now = timezone.now()
        if now > self.end_timestamp:
            return "expired"

        elif self.end_timestamp > now > self.start_timestamp:
            return "ongoing"

        else:
            return "upcoming"
