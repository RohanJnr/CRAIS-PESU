from django.db import models
from django.forms.widgets import Textarea
from django.http import HttpRequest
from modelcluster.models import ClusterableModel, ParentalKey
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.models import Orderable, Page
from wagtail.search import index
from wagtail.snippets.models import register_snippet


class CoursesIndexPage(Page):
    """Page to list all courses."""

    intro = models.CharField(max_length=255)

    content_panels = Page.content_panels + [FieldPanel("intro")]

    parent_page_types = ("base.HomePage",)
    max_count = 1

    def get_context(self, request: HttpRequest, *args, **kwargs) -> dict:
        """List all courses on the page."""
        context = super().get_context(request, *args, **kwargs)

        context["courses"] = Course.objects.all()
        context["course_programs"] = CourseProgram.objects.all()

        return context


class CourseFaculty(Orderable):
    """Faculty conducting the course."""

    model = ParentalKey("content.Course", related_name="faculty")
    faculty = models.ForeignKey(
        "content.Member",
        blank=True,
        on_delete=models.CASCADE,
    )

    panels = [
        FieldPanel("faculty")
    ]

    def __str__(self) -> str:
        return self.faculty.name


@register_snippet
class CourseProgram(ClusterableModel):
    """Programs for courses. Ex: UG, PG."""

    name = models.CharField(max_length=255)

    panels = [
        FieldPanel("name"),
    ]

    class Meta:
        """Order by name."""

        ordering = ("name", )
    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.name

@register_snippet
class Course(index.Indexed, ClusterableModel):
    """Courses offered by CRAIS model."""

    title = models.CharField(max_length=256)
    synopsis = models.TextField()
    credits = models.IntegerField()
    program = models.ForeignKey(
        CourseProgram,
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    panels = [
        FieldPanel("title"),
        FieldPanel("synopsis", widget=Textarea),
        FieldPanel("credits"),
        FieldPanel('program'),
        MultiFieldPanel(
            [InlinePanel("faculty", min_num=1, label="Faculty")],
            heading="Course Faculty",
        ),
    ]

    parent_page_types = ("content.CoursesIndexPage",)
