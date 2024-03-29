from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField
from wagtail.models import Page

from .news_index_page import NewsIndexPage


class NewsPage(Page):
    """Page for individual news post."""

    parent_page_types = (NewsIndexPage,)

    posted_at = models.DateField(auto_now=True)
    body = RichTextField(blank=True)
    author = models.ForeignKey("content.Member", null=True, blank=True, on_delete=models.SET_NULL, related_name="+")
    pinned = models.BooleanField(default=False, help_text="Pins the post on top the page.")

    content_panels = Page.content_panels + [
        FieldPanel("body"),
        FieldPanel("author"),
        FieldPanel("pinned"),
    ]
