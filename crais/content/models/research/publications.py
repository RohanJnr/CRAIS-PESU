from django.db import models
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.models import Orderable
from wagtail.search import index
from wagtail.snippets.models import register_snippet

PUBLICATION_CATEGORY_CHOICES = (
    ("conference", "Conference"),
    ("journal", "Journal"),
    ("book chapter", "Book Chapter")
)


class CenterAuthor(Orderable):
    """Publication authors from CRAIS."""

    model = ParentalKey("content.Publication", related_name="center_authors")
    author = models.ForeignKey(
        "content.Member",
        blank=True,
        on_delete=models.CASCADE,
    )

    panels = [
        FieldPanel("author")
    ]

    def __str__(self) -> str:
        return self.author.name


class ExternalAuthor(Orderable):
    """External publications authors."""

    model = ParentalKey("content.Publication", related_name="external_authors")
    author = models.CharField(max_length=255)

    panels = [
        FieldPanel("author")
    ]

    def __str__(self) -> str:
        return self.author


@register_snippet
class Publication(index.Indexed, ClusterableModel):
    """Model for research publication."""

    title = models.CharField(max_length=512)
    date = models.DateField()
    publication_category = models.CharField(
        max_length=64,
        choices=PUBLICATION_CATEGORY_CHOICES
    )

    link = models.URLField(blank=True, null=True)

    panels = [
        FieldPanel("title"),
        FieldPanel("date"),
        FieldPanel("publication_category"),
        FieldPanel("link"),
        MultiFieldPanel(
            [InlinePanel("center_authors", min_num=1, label="Center Authors")],
            heading="Center Authors",
        ),
        MultiFieldPanel(
            [InlinePanel("external_authors", label="External Authors")],
            heading="External Authors",
        ),
    ]

    class Meta:
        """Order publications of date."""

        ordering = ("date", )


    def __str__(self) -> str:
        return self.title
