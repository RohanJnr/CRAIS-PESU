from dataclasses import Field
from django import forms
from django.db import models
from modelcluster.models import ClusterableModel
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.search import index
from wagtail.snippets.models import register_snippet


@register_snippet
class MemberCategory(index.Indexed, models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(
        max_length=512,
        blank=True,
        null=True
    )

    panels = [
        FieldPanel("name"),
        FieldPanel("description", widget=forms.Textarea),
    ]

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Member Category"
        verbose_name_plural = "Member Categories"
        ordering = ("name", )

@register_snippet
class BaseMember(index.Indexed, ClusterableModel):
    name = models.CharField(max_length=255)
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    email = models.EmailField()

    linkedin_link = models.URLField(
        blank=True,
        null=True,
    )
    google_scholar_link = models.URLField(
        blank=True,
        null=True,
    )

    panels = [
        FieldPanel("name"),
        FieldPanel("image"),
        FieldPanel("linkedin_link"),
        FieldPanel("google_scholar_link"),
    ]


    def __str__(self) -> str:
        return self.name


@register_snippet
class Member(BaseMember):
    category = models.ForeignKey(
        "users.MemberCategory", blank=True, null=True, on_delete=models.SET_NULL
    )
    pes_faculty_profile_link = models.URLField(
        blank=True,
        null=True,
    )

    panels = BaseMember.panels + [
        FieldPanel("category"),
        FieldPanel("pes_faculty_profile_link"),
    ]


@register_snippet
class Intern(BaseMember):
    faculty_guide = models.ForeignKey(
        "users.Member",
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    srn = models.CharField(
        max_length=32,
        blank=True,
        null=True,
        help_text="Enter srn if applicable"
    )
    university = models.CharField(max_length=128)

    panels = BaseMember.panels + [
        FieldPanel("faculty_guide"),
        FieldPanel("srn"),
        FieldPanel("university")
    ]

