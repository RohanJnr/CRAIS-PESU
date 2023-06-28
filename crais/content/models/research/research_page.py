from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField
from wagtail.models import Page

from .patents import Patent
from .publications import Publication


class ResearchPage(Page):
    intro = models.CharField(max_length=255)
    information = RichTextField()

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
        FieldPanel("information"),
    ]

    parent_page_types = ("base.HomePage",)
    max_count = 1

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)


        if category := request.GET.get("publication_category"):
            if category != "all":
                publications = Publication.objects.filter(publication_category=category)
                context["publications"] = publications
                return context

        if year := request.GET.get("publication_year"):
            print(year, type(year))
            publications = Publication.objects.filter(date__year=int(year))
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
