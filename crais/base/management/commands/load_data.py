from django.core.management.base import BaseCommand
from wagtail.models import Page, Site

from crais.base.models import AboutPage, FormPage, FormField, HomePage
from crais.projects.models import ProjectIndexPage
from crais.users.models import MemberCategory


class Command(BaseCommand):
    """
    Remove default wagtail site and root page and create new pages and site instances.
    """

    def handle(self, *args, **options) -> None:
        if Page.objects.count() != 2:
            return

        if Site.objects.filter(hostname='localhost').exists():
            Site.objects.get(hostname='localhost').delete()
        if Page.objects.filter(title='Welcome to your new Wagtail site!').exists():
            Page.objects.get(title='Welcome to your new Wagtail site!').delete()

        root_page: Page = Page.objects.get(pk=1)

        home_page = HomePage(
            title="Home Page",
            intro="This is intro",
            about_us="About us description",
            slug="home"
        )

        root_page.add_child(instance=home_page)
        home_page.save()

        project_index_page = ProjectIndexPage(
            title="Projects and Events",
            intro="Projects by CRAIS of PES University.",
            slug="projects"
        )

        home_page.add_child(instance=project_index_page)
        project_index_page.save()

        Site.objects.create(
            hostname="localhost",
            port=8000,
            site_name="CRAIS PESU Site",
            root_page=home_page,
            is_default_site=True
        )

        about_page = AboutPage(
            title="About Us",
            intro=(
                "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc consequat "
                "ligula nisl, ultrices accumsan lectus tincidunt ac. "
            ),
            body=(
                "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc consequat "
                "ligula nisl, ultrices accumsan lectus tincidunt ac. "
            ),
            slug="about-us"
        )

        home_page.add_child(instance=about_page)
        about_page.save()

        # Create contact page
        contact_page = FormPage(
            title="Contact Us",
            intro=(
                "We'd love to hear from you! Drop us a line to let us know what you liked or didn't like about "
                "your recent store visit, or if you have comments or questions about this site."
            ),
            thank_you_text="Thank you for the submission! We will get back to you soon!",
            form_fields=[
                FormField(label="Name", field_type="singleline"),
                FormField(label="Email", field_type="email"),
                FormField(label="Phone", field_type="number"),
                FormField(label="Message", field_type="multiline")
            ]
        )

        home_page.add_child(instance=contact_page)
        contact_page.save()

        MemberCategory.objects.create(
            name="Faculty"
        )
        MemberCategory.objects.create(
            name="PhD Scholar"
        )
        MemberCategory.objects.create(
            name="Research Assistant"
        )
