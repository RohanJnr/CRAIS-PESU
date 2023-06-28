from django.db import models
from django.http import HttpRequest
from wagtail.admin.panels import FieldPanel
from wagtail.models import Page

from .project_page import ProjectCategory, ProjectPage


class ProjectIndexPage(Page):
    intro = models.CharField(max_length=255)

    content_panels = Page.content_panels + [FieldPanel("intro")]

    parent_page_types = ("base.HomePage",)
    subpage_types = ("content.ProjectPage",)
    max_count = 1

    def get_context(self, request: HttpRequest, *args, **kwargs) -> dict:
        """Update context to include only published posts, ordered by reverse-chron."""
        context = super().get_context(request)

        project_pages = self.get_children().live().order_by("-first_published_at")

        project_years = ProjectPage.objects.order_by().values('date').distinct()
        project_categories = ProjectCategory.objects.all()

        context["projectpages"] = project_pages
        context["project_years"] = project_years
        context["project_categories"] = project_categories
        return context
