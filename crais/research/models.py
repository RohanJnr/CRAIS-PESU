from atexit import register
from dataclasses import Field
from django.db import models
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.fields import RichTextField
from wagtail.models import Orderable, Page
from wagtail.search import index
from wagtail.snippets.models import register_snippet


@register_snippet
class ResearchTopic(index.Indexed, ClusterableModel):
    title = models.CharField(max_length=255)
    details = RichTextField()

    panels = [
        FieldPanel("title"),
        FieldPanel("details")
    ]


class ResearchPage(Page):
    information = RichTextField()


# class ResearchAuthors(Orderable):

#     page = ParentalKey("research.Base", related_name="authors")
#     author = models.ForeignKey(
#         "users.BaseMember",
#         blank=True,
#         on_delete=models.CASCADE,
#     )

#     panels = [
#         FieldPanel("author")
#     ]


class Base(index.Indexed, models.Model):
    title = models.CharField(max_length=512)
    published = models.DateField()
    link = models.URLField(
        help_text="DOI link"
    )

    panels = [
        FieldPanel("title"),
        FieldPanel("published"),
        FieldPanel("link")
    ]

@register_snippet
class Publication(Base):

    type_of_publication = models.CharField(max_length=255)  

    panels = Base.panels + [
        FieldPanel("type_of_publication")
    ]

@register_snippet
class Patent(Base):
    
    type_of_patent = models.CharField(max_length=255)

    panels = Base.panels + [
        FieldPanel("type_of_patent")
    ]

