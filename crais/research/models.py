from atexit import register
from dataclasses import Field
from secrets import choice
from sre_parse import CATEGORIES
from django.db import models
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.fields import RichTextField
from wagtail.models import Orderable, Page
from wagtail.search import index
from wagtail.snippets.models import register_snippet


PUBLICATION_CATEGORY_CHOICES = (
    ("conference", "Conference"),
    ("journal", "Journal")
)

PATENT_STATUS = (
    ("filed", "Filed"),
    ("published", "Published"),
    ("granted", "Granted")
)


@register_snippet
class ResearchTopic(index.Indexed, ClusterableModel):
    title = models.CharField(max_length=255)
    details = RichTextField()

    panels = [
        FieldPanel("title"),
        FieldPanel("details")
    ]


class ResearchPage(Page):
    intro = models.CharField(max_length=255)
    information = RichTextField()

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
        FieldPanel("information"),
    ]

    parent_page_types = ("base.HomePage",)

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)


        if category := request.GET.get("publication_category"):
            if category != "all":
                publications = Publication.objects.filter(publication_category=category)
                context["publications"] = publications
                return context

        if year := request.GET.get("publication_year"):
            print(year, type(year))
            publications = publications.filter(date__year=int(year))
            context["publications"] = publications
            return context

        publications = Publication.objects.all()
        pub_dates = Publication.objects.dates('date', 'year')



        patents = Patent.objects.all()

        context["publications"] = publications
        context["patents"] = patents
        context["pub_dates"] = pub_dates

        return context
    
    def get_template(self, request, *args, **kwargs):
        template = super().get_template(request, *args, **kwargs)

        if request.GET.get("publication_category") or request.GET.get("publication_year"):
            return "research/_partials/publications.html"
        
        return template


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


class CenterAuthor(Orderable):
    model = ParentalKey("research.Publication", related_name="center_authors")
    author = models.ForeignKey(
        "users.BaseMember",
        blank=True,
        on_delete=models.CASCADE,
    )

    panels = [
        FieldPanel("author")
    ]

    def __str__(self) -> str:
        return self.author.name


class ExternalAuthor(Orderable):
    model = ParentalKey("research.Publication", related_name="external_authors")
    author = models.CharField(max_length=255)

    panels = [
        FieldPanel("author")
    ]

    def __str__(self) -> str:
        return self.author

class CenterInventor(Orderable):
    model = ParentalKey("research.Patent", related_name="center_inventors")
    inventor = models.ForeignKey(
        "users.BaseMember",
        blank=True,
        on_delete=models.CASCADE,
    )

    panels = [
        FieldPanel("inventor")
    ]

    def __str__(self) -> str:
        return self.inventor.name


class ExternalInventor(Orderable):
    model = ParentalKey("research.Patent", related_name="external_inventors")
    inventor = models.CharField(max_length=255)

    panels = [
        FieldPanel("inventor")
    ]
    
    def __str__(self) -> str:
        return self.inventor


@register_snippet
class Publication(index.Indexed, ClusterableModel):
    title = models.CharField(max_length=512)
    date = models.DateField()
    publication_details = RichTextField()
    publication_category = models.CharField(
        max_length=64,
        choices=PUBLICATION_CATEGORY_CHOICES
    )

    link = models.URLField()
    
    panels = [
        FieldPanel("title"),
        FieldPanel("date"),
        FieldPanel("publication_details"),
        FieldPanel("publication_category"),
        FieldPanel("link"),
        MultiFieldPanel(
            [InlinePanel("center_authors", min_num=1, label="Center Authors")],
            heading="Center Authors",
        ),
        MultiFieldPanel(
            [InlinePanel("external_authors", min_num=1, label="External Authors")],
            heading="External Authors",
        ),
    ]

    class Meta:
        ordering = ("date", )


    def __str__(self) -> str:
        return self.title

@register_snippet
class Patent(index.Indexed, ClusterableModel):
    title = models.CharField(max_length=512)
    date = models.DateField()
    status = models.CharField(
        max_length=64,
        choices=PATENT_STATUS
    )
    link = models.URLField()
    
    panels = [
        FieldPanel("title"),
        FieldPanel("date"),
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
        ordering = ("date", )

    def __str__(self) -> str:
        return self.title