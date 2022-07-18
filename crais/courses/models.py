from django.db import models
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.fields import RichTextField
from wagtail.models import Page, Orderable
from wagtail.search import index
from wagtail.snippets.models import register_snippet


class CourseIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [FieldPanel("intro")]

    parent_page_types = ("base.HomePage",)


class CourseFaculty(Orderable):

    page = ParentalKey("courses.CoursePage", related_name="faculties")
    faculty = models.ForeignKey(
        "users.Member",
        blank=True,
        on_delete=models.CASCADE,
    )

    panels = [
        FieldPanel("faculty")
    ]


@register_snippet
class CourseProgram(index.Indexed, ClusterableModel):
    name = models.CharField(max_length=255)

    panels = [
        FieldPanel("name"),
    ]

    def __str__(self) -> str:
        return self.name


class CoursePage(Page):
    synopsis = RichTextField()
    credits = models.IntegerField()
    program = models.ForeignKey(
        "courses.CourseProgram",
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    content_panels = Page.content_panels + [
        FieldPanel("title"),
        FieldPanel("synopsis"),
        FieldPanel("credits"),
        FieldPanel('program'),
        MultiFieldPanel(
            [InlinePanel("faculties", min_num=1, label="Faculties")],
            heading="Course faculties",
        ),
    ]
