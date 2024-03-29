from django.db import models
from django.core.exceptions import ValidationError
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.models import Orderable
from wagtail.search import index
from wagtail.snippets.models import register_snippet

PATENT_STATUS = (
    ("filed", "Filed"),
    ("published", "Published"),
    ("granted", "Granted")
)


class CenterInventor(Orderable):
    """Patent inventor from CRAIS."""

    model = ParentalKey("content.Patent", related_name="center_inventors")
    inventor = models.ForeignKey(
        "content.Member",
        blank=True,
        on_delete=models.CASCADE,
    )

    panels = [
        FieldPanel("inventor")
    ]

    def __str__(self) -> str:
        return self.inventor.name


class ExternalInventor(Orderable):
    """External patient inventor."""

    model = ParentalKey("content.Patent", related_name="external_inventors")
    inventor = models.CharField(max_length=255)

    panels = [
        FieldPanel("inventor")
    ]

    def __str__(self) -> str:
        return self.inventor



@register_snippet
class Patent(index.Indexed, ClusterableModel):
    """Patents filed by CRAIS."""

    title = models.CharField(max_length=512)
    date_filed = models.DateField()
    date_granted = models.DateField(blank=True, null=True)
    status = models.CharField(
        max_length=64,
        choices=PATENT_STATUS
    )
    link = models.URLField(blank=True, null=True)

    panels = [
        FieldPanel("title"),
        FieldPanel("date_filed"),
        FieldPanel("date_granted"),
        FieldPanel("status"),
        FieldPanel("link"),
        MultiFieldPanel(
            [InlinePanel("center_inventors", min_num=1, label="Center Inventors")],
            heading="Center Inventors",
        ),
        MultiFieldPanel(
            [InlinePanel("external_inventors", min_num=1, label="External Inventors")],
            heading="External Inventors"
        ),
    ]

    class Meta:
        """Order patents by date_filed."""

        ordering = ("date_filed", )

    def clean(self) -> None:
        """Validate data before saving."""
        if self.date_granted is not None and self.status == "filed":
            raise ValidationError("Cannot assign status 'Filed' for a patent with granted date.")

        super().clean()


    def __str__(self) -> str:
        return self.title
