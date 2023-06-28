from django.db import models
from django.http import HttpRequest
from modelcluster.models import ClusterableModel
from wagtail.admin.panels import FieldPanel
from wagtail.models import Page
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

        return context


# class CourseFaculty(Orderable):

#     model = ParentalKey("courses.Course", related_name="faculties")
#     faculty = models.ForeignKey(
#         "users.Member",
#         blank=True,
#         on_delete=models.CASCADE,
#     )

#     panels = [
#         FieldPanel("faculty")
#     ]

#     def __str__(self) -> str:
#         return self.faculty.name


@register_snippet
class CourseProgram(ClusterableModel):
    """Programs for courses. Ex: UG, PG."""

    name = models.CharField(max_length=255)

    panels = [
        FieldPanel("name"),
    ]

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
        FieldPanel("synopsis"),
        FieldPanel("credits"),
        FieldPanel('program'),
    ]

    parent_page_types = ("content.CoursesIndexPage",)
