from django.db import models
from django.utils.text import slugify
from modelcluster.models import ClusterableModel
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField
from wagtail.search import index
from wagtail.snippets.models import register_snippet


@register_snippet
class MemberCategory(models.Model):
    """Categories for members. Ex: Faculty, Intern, Research Associate, etc."""

    name = models.CharField(max_length=255)
    description = RichTextField(null=True, blank=True)

    panels = [
        FieldPanel("name"),
        FieldPanel("description"),
    ]

    class Meta:
        """Order objects by name."""

        verbose_name = "Member Category"
        verbose_name_plural = "Member Categories"

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.name



@register_snippet
class Member(index.Indexed, ClusterableModel):
    """Member model for users/researchers CRAIS."""

    name = models.CharField(max_length=255)
    about = RichTextField(help_text="About the member.")
    slug = models.SlugField(
        default="",
        editable=False,
        max_length=255
    )
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    email = models.EmailField()

    linkedin_link = models.URLField(
        blank=True,
        null=True,
    )
    google_scholar_link = models.URLField(
        blank=True,
        null=True,
    )
    category = models.ForeignKey(
        "content.MemberCategory", blank=True, null=True, on_delete=models.SET_NULL, related_name="members"
    )
    designation = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text="Ignore this field if 'category' is sufficient."
    )

    pes_faculty_profile_link = models.URLField(
        blank=True,
        null=True,
    )

    faculty_guide = models.ForeignKey(
        "content.Member",
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    srn = models.CharField(
        max_length=32,
        blank=True,
        null=True,
        help_text="Enter srn if applicable"
    )
    university = models.CharField(max_length=128)

    member_page = models.BooleanField(
        default=True,
        help_text="Generates a page at /team/<name> with details for the member."
    )

    panels = [
        FieldPanel("name"),
        FieldPanel("about"),
        FieldPanel("image"),
        FieldPanel("linkedin_link"),
        FieldPanel("google_scholar_link"),
        FieldPanel("category"),
        FieldPanel("designation"),
        FieldPanel("pes_faculty_profile_link"),
        FieldPanel("faculty_guide"),
        FieldPanel("srn"),
        FieldPanel("university")
    ]

    search_fields = [
        index.FilterField("name"),
        index.FilterField("university"),
        index.FilterField("srn"),
    ]

    def __str__(self) -> str:
        return self.name

    def save(self, **kwargs) -> None:
        """Override save method to save slug field."""
        name = self.name
        self.slug = slugify(name)
        super().save(**kwargs)
