from django.contrib.auth.models import User
from django.db import models
from django.http import HttpRequest
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from wagtail.core.fields import RichTextField
from wagtail.models import Page
from wagtail.search import index

from wagtail.documents import get_document_model


class NewsIndexPage(Page):
    intro = models.CharField(max_length=256)
    content_panels = Page.content_panels + [FieldPanel("intro", classname="full")]

    parent_page_types = ("base.HomePage",)
    subpage_types = ("news.NewsPage",)
    max_count = 1

    def get_context(self, request: HttpRequest, *args, **kwargs) -> dict:
        """Update context to include only published posts, ordered by reverse-chron."""
        context = super().get_context(request)
        news_posts = self.get_children().live().order_by("-first_published_at")
        context["news_posts"] = news_posts
        return context


class NewsPage(Page):
    posted_at = models.DateField(auto_now=True)
    body = RichTextField(blank=True)
    featured = models.BooleanField(default=False)

    content_panels = Page.content_panels + [
        FieldPanel("body", classname="full"),
        FieldPanel("featured"),
    ]

    parent_page_types = (NewsIndexPage,)


class NewsModelAdmin(ModelAdmin):
    model = NewsPage
    menu_label = "News posts"
    menu_icon = "list-ul"
    menu_order = 200
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("title",)
    list_filter = ("featured",)


modeladmin_register(NewsModelAdmin)
