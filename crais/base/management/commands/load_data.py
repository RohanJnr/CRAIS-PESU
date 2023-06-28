from django.core.management.base import BaseCommand
from wagtail.models import Page, Site

from crais.base.models import AboutPage, FormField, HomePage, ContactPage
from crais.events.models import EventIndexPage
from crais.projects.models import ProjectIndexPage
from crais.research.models import ResearchPage
from crais.courses.models import CoursesIndexPage
from crais.users.models import MemberCategory


class Command(BaseCommand):
    """Remove default wagtail site and root page and create new pages and site instances."""

    def handle(self, *args, **options) -> None:
        """The actual logic of the command."""
        if Page.objects.count() != 2:
            return

        if Site.objects.filter(hostname='localhost').exists():
            Site.objects.get(hostname='localhost').delete()
        if Page.objects.filter(title='Welcome to your new Wagtail site!').exists():
            Page.objects.get(title='Welcome to your new Wagtail site!').delete()

        root_page: Page = Page.objects.get(pk=1)

        home_page = HomePage(
            title="Home Page",
            about_us_title="title",
            about_us_tagline="tagline",
            about_us_body="body",
            intro="This is intro",
            slug="home"
        )

        root_page.add_child(instance=home_page)
        home_page.save()

        # Create projects page
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

        # Create about page
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

        # Create research page
        research_page = ResearchPage(
            title="About Us",
            intro=(
                "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc consequat "
                "ligula nisl, ultrices accumsan lectus tincidunt ac. "
            ),
            information="Information",
            slug="research"
        )

        home_page.add_child(instance=research_page)
        research_page.save()

        # Courses Page
        courses_page = CoursesIndexPage(
            title="Courses",
            intro=(
                "Courses offered by us!"
            ),
            slug="courses"
        )

        home_page.add_child(instance=courses_page)
        courses_page.save()

        # events Page
        events_page = EventIndexPage(
            title="Events",
            intro=(
                "Courses offered by us!"
            ),
            slug="events"
        )

        home_page.add_child(instance=events_page)
        events_page.save()



        # Create contact page
        contact_page = ContactPage(
            title="Contact Us",
            intro=(
                "We'd love to hear from you! Drop us a line to let us know what you liked or didn't like about "
            ),
            thank_you_text="Thank you for the submission! We will get back to you soon!",
            general_information="Information",
            contact_email="rais@pes.edu",
            contact_phone="9876543210",
            contact_address="address",
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
