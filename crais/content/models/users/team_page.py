from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.models import Orderable, Page
from wagtail.admin.panels import InlinePanel, MultiFieldPanel


class MemberCategoryOrder(Orderable):
    """Category to which member belongs to."""

    page = ParentalKey("content.TeamPage", on_delete=models.SET_NULL, related_name='member_categories' , null=True)
    category = models.ForeignKey("content.MemberCategory", on_delete=models.CASCADE)


class TeamPage(Page):
    """Page to list all members."""

    max_count = 1
    parent_page_types = ("base.HomePage",)

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [InlinePanel("member_categories", label="Member Categories")],
            heading="Member Categories.",
        ),
    ]
