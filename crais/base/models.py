from django.db import models
from django.template.response import TemplateResponse
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import (
    FieldPanel,
    InlinePanel,
)
from wagtail.contrib.forms.models import AbstractForm, AbstractFormField
from wagtail.fields import RichTextField
from wagtail.models import Page

from crais.users.models import Member



class FormField(AbstractFormField):
    page = ParentalKey('FormPage', on_delete=models.CASCADE, related_name='form_fields')


class FormPage(AbstractForm):
    intro = models.CharField(max_length=128)
    thank_you_text = models.CharField(max_length=255)
    general_information = RichTextField()


    content_panels = AbstractForm.content_panels + [
        FieldPanel('intro'),
        FieldPanel('general_information'),
        InlinePanel('form_fields', label="Form fields"),
        FieldPanel('thank_you_text', classname="full"),
    ]

    parent_page_types = ("events.EventPage",)

    def serve(self, request, *args, **kwargs):
        if request.method == "POST":
            form = self.get_form(
                request.POST, request.FILES, page=self, user=request.user
            )

            if form.is_valid():
                form_submission = self.process_form_submission(form)
                return self.render_landing_page(
                    request, form_submission, *args, **kwargs
                )
            
            else:
                context = self.get_context(request)
                context["form"] = form
                return TemplateResponse(request, "base/partial_form_page.html", context)

        else:
            form = self.get_form(page=self, user=request.user)

        context = self.get_context(request)
        context["form"] = form
        return TemplateResponse(request, self.get_template(request), context)


class ContactPage(FormPage):
    contact_email = models.CharField(max_length=255)
    contact_phone = models.CharField(max_length=12)
    contact_address = models.TextField()

    parent_page_types = ("base.HomePage",)


    content_panels = FormPage.content_panels + [
        FieldPanel('contact_email'),
        FieldPanel('contact_phone'),
        FieldPanel('contact_address')
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
    intro = models.CharField(max_length=512)
    body = RichTextField()

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
        FieldPanel("body")
    ]

    parent_page_types = ("base.HomePage",)

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        context["team"] = Member.objects.all().order_by("category")

        return context
