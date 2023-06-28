from wagtail.contrib.modeladmin.options import (
    ModelAdmin, ModelAdminGroup, modeladmin_register
)

from crais.content.models import Course, CourseProgram
from crais.content.models import EventPage
from crais.content.models import Member, MemberCategory
from crais.content.models import ProjectPage, ProjectCategory
from crais.content.models import Patent, Publication
from crais.content.models import NewsPage


class MemberModelAdmin(ModelAdmin):
    model = Member
    menu_label = "Members"
    menu_icon = 'user'
    menu_order = 500
    list_display = ("name", "category")
    list_filter = ("category",)
    search_fields = ("name",)


class ProjectModelAdmin(ModelAdmin):
    model = ProjectPage
    menu_label = "Projects"
    list_display = ("title", "category", "tags", "status")
    list_filter = ("category", "tags", "pinned")
    search_fields = ("title", "intro", "description")


class EventModelAdmin(ModelAdmin):
    model = EventPage
    menu_label = "Events"
    list_display = ("title", "timestamp", "location")
    search_fields = ("title", "intro", "description")
    list_filter = ("featured",)
    add_to_settings_menu = False
    exclude_from_explorer = False


class ContentAdminModel(ModelAdminGroup):
    menu_label = "Content"
    menu_icon = "folder-open-inverse"
    menu_order = 101
    items = (ProjectModelAdmin, EventModelAdmin)

class PublicationModelAdmin(ModelAdmin):
    model = Publication
    menu_label = "Publications"
    list_display = ("title", "date", "publication_category", "link")
    search_fields = ("title", "date", "publication_details", "link", "center_authors", "external_authors")


class PatentModelAdmin(ModelAdmin):
    model = Patent
    menu_label = "Patents"
    list_display = ("title", "date_filed", "status",)
    search_fields = ("title", "date_filed", "status", "center_authors", "external_authors")


class ResearchModelAdminGroup(ModelAdminGroup):
    menu_label = "Research"
    menu_icon = "folder-open-inverse"
    menu_order = 102
    items = (PatentModelAdmin, PublicationModelAdmin)

class CoursesModelAdmin(ModelAdmin):
    model = Course
    menu_label = "Courses"
    menu_order = 103
    list_display = ("title", "synopsis", "credits", "program")
    search_fields = ("title", "synopsis")


class NewsModelAdmin(ModelAdmin):
    model = NewsPage
    menu_label = "News"
    menu_icon = "list-ul"
    menu_order = 104
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("title",)
    list_filter = ("pinned",)


modeladmin_register(NewsModelAdmin)
modeladmin_register(MemberModelAdmin)
modeladmin_register(ContentAdminModel)
modeladmin_register(ResearchModelAdminGroup)
modeladmin_register(CoursesModelAdmin)
