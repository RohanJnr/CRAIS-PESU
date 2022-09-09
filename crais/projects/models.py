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
from wagtail.snippets.widgets import AdminSnippetChooser, AdminChooser

from crais.users.models import BaseMember


PROJECT_STATUS_CHOICES = (
    ("Completed", "COMPLETED"),
    ("Active", "ACTIVE")
)


class ProjectIndexPage(Page):
    intro = models.CharField(max_length=255)

    content_panels = Page.content_panels + [FieldPanel("intro")]

    parent_page_types = ("base.HomePage",)
    subpage_types = ("projects.ProjectPage",)
    max_count = 1

    def get_context(self, request: HttpRequest, *args, **kwargs) -> dict:
        """Update context to include only published posts, ordered by reverse-chron."""
        context = super().get_context(request)

        projectpages = self.get_children().live().order_by("-first_published_at")

        project_years = ProjectPage.objects.order_by().values('date').distinct()

        context["projectpages"] = projectpages
        context["project_years"] = project_years
        return context


class ProjectImages(Orderable):
    """Between 1 and 5 images for the home page carousel."""

    page = ParentalKey("projects.ProjectPage", related_name="project_images")
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    panels = [FieldPanel("image")]


class ProjectContributors(Orderable):

    page = ParentalKey("projects.ProjectPage", related_name="contributors")
    contributor = models.ForeignKey(
        "users.BaseMember",
        blank=True,
        on_delete=models.CASCADE,
    )

    panels = [
        FieldPanel("contributor")
    ]

    def __str__(self) -> str:
        return self.contributor.name


@register_snippet
class ProjectCategory(index.Indexed, models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=512)
    slug = models.SlugField(
        max_length=255,
        help_text="Path for category."
    )

    panels = [
        FieldPanel("name"),
        FieldPanel("description", widget=forms.Textarea),
        FieldPanel("slug"),
    ]

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Project Category"
        verbose_name_plural = "Project Categories"


class ProjectTag(TaggedItemBase):
    content_object = ParentalKey('projects.ProjectPage', on_delete=models.CASCADE, related_name='tagged_items')


class ProjectPage(Page):
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
        "projects.ProjectCategory", blank=True, null=True, on_delete=models.SET_NULL
    )

    tags = ClusterTaggableManager(through=ProjectTag, blank=True)

    date = models.DateField(blank=True, null=True)

    status = models.CharField(max_length=32, choices=PROJECT_STATUS_CHOICES)

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
        FieldPanel("description"),
        FieldPanel("banner"),
        FieldPanel('category'),
        FieldPanel('tags'),
        FieldPanel("date"),
        FieldPanel("status"),
        MultiFieldPanel(
            [InlinePanel("contributors", min_num=1, label="Contributors")],
            heading="Project Contributors",
        ),
    ]

    parent_page_types = ("projects.ProjectIndexPage",)
