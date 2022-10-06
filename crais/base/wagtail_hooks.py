from wagtail.contrib.modeladmin.options import (
    ModelAdmin, ModelAdminGroup, modeladmin_register
)

from crais.courses.models import Course, CourseProgram
from crais.events.models import EventPage
from crais.users.models import Intern, Member, MemberCategory
from crais.projects.models import ProjectPage, ProjectCategory
from crais.research.models import Patent, Publication


class MemberCategoryAdmin(ModelAdmin):
    model = MemberCategory
    menu_label = "Member Categories"


class ProjectCategoryAdmin(ModelAdmin):
    model = ProjectCategory
    menu_label = "Project Categories"

class CourseProgramAdmin(ModelAdmin):
    model = CourseProgram
    menu_label = "Course Programs"


class CategoryModelAdminGroup(ModelAdminGroup):
    menu_label = "Categories"
    menu_icon = "folder-open-inverse"
    menu_order = 400
    items = (MemberCategoryAdmin, ProjectCategoryAdmin, CourseProgramAdmin)


class MemberModelAdmin(ModelAdmin):
    model = Member
    menu_label = "Members"
    menu_icon = 'user'
    menu_order = 200
    list_display = ("name", "category")
    list_filter = ("category",)
    search_fields = ("name",)

class InternModelAdmin(ModelAdmin):
    model = Intern
    menu_label = "Interns"
    menu_icon = 'user'
    menu_order = 200
    list_display = ("name", "university", "srn", "faculty_guide")
    list_filter = ("university", "faculty_guide")
    search_fields = ("name", "university", "srn", "faculty_guide")


class TeamAdminModel(ModelAdminGroup):
    menu_label = "Team"
    menu_icon = "folder-open-inverse"
    menu_order = 300
    items = (MemberModelAdmin, InternModelAdmin)


class ProjectModelAdmin(ModelAdmin):
    model = ProjectPage
    menu_label = "Projects"
    list_display = ("title", "category", "tags", "status")
    list_filter = ("category", "tags", "featured")
    search_fields = ("title", "intro", "description")


class EventModelAdmin(ModelAdmin):
    model = EventPage
    menu_label = "Events"
    list_display = ("title", "timestamp", "venue")
    search_fields = ("title", "intro", "description")
    list_filter = ("featured",)


class ContentAdminModel(ModelAdminGroup):
    menu_label = "Content"
    menu_icon = "folder-open-inverse"
    menu_order = 300
    items = (ProjectModelAdmin, EventModelAdmin)

class PublicationModelAdmin(ModelAdmin):
    model = Publication
    menu_label = "Publications"
    list_display = ("title", "date", "publication_category", "link")
    search_fields = ("title", "date", "publication_details", "link", "center_authors", "external_authors")


class PatentModelAdmin(ModelAdmin):
    model = Patent
    menu_label = "Patents"
    list_display = ("title", "date", "status",)
    search_fields = ("title", "date", "status", "center_authors", "external_authors")


class ResearchModelAdminGroup(ModelAdminGroup):
    menu_label = "Research"
    menu_icon = "folder-open-inverse"
    menu_order = 400
    items = (PatentModelAdmin, PublicationModelAdmin)

class CoursesModelAdmin(ModelAdmin):
    model = Course
    menu_label = "Courses"
    menu_order = 400
    list_display = ("title", "synopsis", "credits", "program")
    search_fields = ("title", "synopsis")


modeladmin_register(CategoryModelAdminGroup)
modeladmin_register(TeamAdminModel)
modeladmin_register(ContentAdminModel)
modeladmin_register(ResearchModelAdminGroup)
modeladmin_register(CoursesModelAdmin)
    