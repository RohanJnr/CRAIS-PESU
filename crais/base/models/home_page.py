from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel
from wagtail.models import Orderable, Page


class HomePageFeatured(Orderable):
    """Featured news or information on home page."""

    page = ParentalKey("base.HomePage", related_name="featured")
    title = models.CharField(max_length=256)
    link = models.URLField()
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    panels = [
        FieldPanel("title"),
        FieldPanel("link"),
        FieldPanel("image")
    ]

class HomePageOurWork(Orderable):
    """Work done by CRAIS displayed on the home page."""

    page = ParentalKey("base.HomePage", related_name="our_work")
    title = models.CharField(max_length=256)
    short_description = models.CharField(max_length=128)
    link = models.URLField()


    panels = [
        FieldPanel("title"),
        FieldPanel("short_description"),
        FieldPanel("link"),
    ]

class HomePageCollaborations(Orderable):
    """Model for industry collaborations of CRAIS."""

    page = ParentalKey("base.HomePage", related_name="collaborations")
    collaborator_name = models.CharField(max_length=128, help_text="Company name, Industry Partner name, etc")
    collaborator_logo = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Company logo"
    )
    collaborator_link = models.URLField(help_text="Link to company website/information.", null=True, blank=True)

    panels = [
        FieldPanel("collaborator_name"),
        FieldPanel("collaborator_logo"),
        FieldPanel("collaborator_link"),
    ]


class HomePage(Page):
    """Home page model."""

    title_part_1 = models.CharField(max_length=64)
    title_part_2 = models.CharField(max_length=64)
    landing_page_paragraph = models.CharField(max_length=312)

    content_panels = Page.content_panels + [
        FieldPanel("title_part_1"),
        FieldPanel("title_part_2"),
        FieldPanel("landing_page_paragraph")
    ]

    max_count = 1
