from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import (
    FieldPanel,
    InlinePanel,
)
from wagtail.contrib.forms.models import AbstractForm, AbstractFormField
from wagtail.fields import RichTextField
from wagtail.models import Page



class FormField(AbstractFormField):
    page = ParentalKey('FormPage', on_delete=models.CASCADE, related_name='form_fields')


class FormPage(AbstractForm):
    intro = RichTextField(blank=True)
    thank_you_text = RichTextField(blank=True)

    content_panels = AbstractForm.content_panels + [
        FieldPanel('intro', classname="full"),
        InlinePanel('form_fields', label="Form fields"),
        FieldPanel('thank_you_text', classname="full"),
    ]


class HomePage(Page):
    intro = models.TextField()
    about_us = RichTextField()
    image_1 = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
        FieldPanel("about_us"),
        FieldPanel("image_1"),
    ]

    max_count = 1


class AboutPage(Page):
    intro = RichTextField()

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
    ]

    parent_page_types = ("base.HomePage",)
