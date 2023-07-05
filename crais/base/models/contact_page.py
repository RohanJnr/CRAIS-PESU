from .form_page import FormPage


class ContactPage(FormPage):
    """Model for contact page with contact form."""

    max_count = 1
    parent_page_types = ("base.HomePage",)
