from django.db import models
from django.http import HttpRequest
from wagtail.admin.panels import FieldPanel
from wagtail.models import Page

from .project_page import ProjectCategory, ProjectPage


class ProjectIndexPage(Page):
    """Page to list all projects by CRAIS."""

    intro = models.CharField(max_length=255)

    content_panels = Page.content_panels + [FieldPanel("intro")]

    parent_page_types = ("base.HomePage",)
    subpage_types = ("content.ProjectPage",)
    max_count = 1

    def get_context(self, request: HttpRequest, *args, **kwargs) -> dict:
        """Update context to include only published posts, ordered by reverse-chron."""
        context = super().get_context(request)

        project_pages = ProjectPage.objects.all().order_by("-start_date")

        project_categories = ProjectCategory.objects.all()

        context["projects"] = project_pages
        context["project_years"] = [project.start_date.year for project in project_pages]
        context["project_categories"] = project_categories
        return context
