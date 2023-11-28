from django.db import models
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey
from taggit.models import TaggedItemBase
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.fields import RichTextField
from wagtail.models import Page, Orderable
from wagtail.search import index
from wagtail.snippets.models import register_snippet


PROJECT_STATUS_CHOICES = (
    ("Completed", "COMPLETED"),
    ("Active", "ACTIVE")
)


class ProjectImages(Orderable):
    """Between 1 and 5 images for the home page carousel."""

    page = ParentalKey("content.ProjectPage", related_name="project_images")
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    panels = [FieldPanel("image")]


class ProjectContributors(Orderable):
    """Members who contributed towards the project."""

    page = ParentalKey("content.ProjectPage", related_name="contributors")
    contributor = models.ForeignKey(
        "content.Member",
        blank=True,
        on_delete=models.CASCADE,
    )

    panels = [
        FieldPanel("contributor")
    ]


@register_snippet
class ProjectCategory(index.Indexed, models.Model):
    """Project categories. Ex: Research, Internship, Capstone, etc."""

    name = models.CharField(max_length=255, unique=True)

    panels = [
        FieldPanel("name"),
    ]

    class Meta:
        """Alter verbose name of model."""

        verbose_name = "Project Category"
        verbose_name_plural = "Project Categories"

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.name


class ProjectTag(TaggedItemBase):
    """Project tags."""

    content_object = ParentalKey('content.ProjectPage', on_delete=models.CASCADE, related_name='tagged_items')


class ProjectPage(Page):
    """Page for projects done by CRAIS."""

    intro = models.CharField(max_length=255)
    description = RichTextField()
    banner = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    category = models.ForeignKey(
        "content.ProjectCategory", blank=True, null=True, on_delete=models.SET_NULL
    )
    tags = ClusterTaggableManager(through=ProjectTag, blank=True)

    start_date = models.DateField(help_text="This field is used for project ordering.")
    end_date = models.DateField(blank=True, null=True, help_text="leave blank if project is not completed.")

    pinned = models.BooleanField(default=False)

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
        FieldPanel("description"),
        FieldPanel("banner"),
        FieldPanel('category'),
        FieldPanel('tags'),
        FieldPanel("start_date"),
        FieldPanel("end_date"),
        FieldPanel("pinned"),
        MultiFieldPanel(
            [InlinePanel("contributors", label="Contributors")],
            heading="Project Contributors",
        ),
        InlinePanel('project_images', label="Gallery images"),
    ]

    parent_page_types = ("content.ProjectIndexPage",)
