from django.db import models
from django.http import HttpRequest
from django.template.response import TemplateResponse
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField


class FormField(AbstractFormField):
    """Form input field linked to forms."""

    page = ParentalKey('FormPage', on_delete=models.CASCADE, related_name='form_fields')


class FormPage(AbstractEmailForm):
    """General form page for registrations and contact page."""

    intro = models.CharField(max_length=128)
    thank_you_text = models.CharField(max_length=255)
    general_information = models.TextField(blank=True, null=True)


    content_panels = AbstractEmailForm.content_panels + [
        FieldPanel('intro'),
        FieldPanel('general_information'),
        InlinePanel('form_fields', label="Form fields"),
        FieldPanel('thank_you_text', classname="full"),
        FieldPanel("from_address"),
        FieldPanel("to_address"),
        FieldPanel("subject")

    ]

    parent_page_types = ("content.EventPage",)

    def serve(self, request: HttpRequest, *args, **kwargs) -> TemplateResponse:
        """Alter form submission response to return a template response which is handled by htmx."""
        if request.method == "POST":
            form = self.get_form(
                request.POST, request.FILES, page=self, user=request.user
            )

            if form.is_valid():
                form_submission = self.process_form_submission(form)
                return self.render_landing_page(
                    request, form_submission, *args, **kwargs
                )

            context = self.get_context(request)
            context["form"] = form
            return TemplateResponse(request, "base/partial_form_page.html", context)

        form = self.get_form(page=self, user=request.user)

        context = self.get_context(request)
        context["form"] = form
        return TemplateResponse(request, self.get_template(request), context)
