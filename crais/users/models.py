from django import forms
from django.db import models
from modelcluster.models import ClusterableModel
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.search import index
from wagtail.snippets.models import register_snippet


@register_snippet
class TeamCategory(index.Indexed, models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=512)

    panels = [
        FieldPanel("name"),
        FieldPanel("description", widget=forms.Textarea),
    ]

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Team Category"
        verbose_name_plural = "Team Categories"


@register_snippet
class Member(index.Indexed, ClusterableModel):
    name = models.CharField(max_length=255)
    designation = models.CharField(max_length=255)
    category = models.ForeignKey(
        "users.TeamCategory", blank=True, null=True, on_delete=models.SET_NULL
    )
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    linkedin_link = models.URLField(
        blank=True,
        null=True,
    )
    pes_faculty_profile_link = models.URLField(
        blank=True,
        null=True,
    )
    google_scholar_link = models.URLField(
        blank=True,
        null=True,
    )

    panels = [
        FieldPanel("name"),
        FieldPanel("designation"),
        FieldPanel("category"),
        FieldPanel("image"),
        FieldPanel("linkedin_link"),
        FieldPanel("pes_faculty_profile_link"),
        FieldPanel("google_scholar_link"),
    ]


    def __str__(self) -> str:
        return self.name
