from django.db import models
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.fields import RichTextField
from wagtail.models import Page, Orderable
from wagtail.search import index
from wagtail.snippets.models import register_snippet


class CoursesIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [FieldPanel("intro")]

    parent_page_types = ("base.HomePage",)

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        context["courses"] = Course.objects.all()

        return context


class CourseFaculty(Orderable):

    model = ParentalKey("courses.Course", related_name="faculties")
    faculty = models.ForeignKey(
        "users.Member",
        blank=True,
        on_delete=models.CASCADE,
    )

    panels = [
        FieldPanel("faculty")
    ]

    def __str__(self) -> str:
        return self.faculty.name


@register_snippet
class CourseProgram(index.Indexed, ClusterableModel):
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
    title = models.CharField(max_length=256)
    synopsis = models.TextField()
    credits = models.IntegerField()
    program = models.ForeignKey(
        "courses.CourseProgram",
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    panels = [
        FieldPanel("title"),
        FieldPanel("synopsis"),
        FieldPanel("credits"),
        FieldPanel('program'),
        MultiFieldPanel(
            [InlinePanel("faculties", min_num=1, label="Faculties")],
            heading="Course faculties",
        ),
    ]

    parent_page_types = ("courses.CoursesIndexPage",)