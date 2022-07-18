from wagtail.contrib.modeladmin.options import (
    ModelAdmin, ModelAdminGroup, modeladmin_register
)

from crais.users.models import Intern, Member, MemberCategory
from crais.projects.models import ProjectPage, ProjectCategory
from crais.research.models import Publication, Patent


class MemberCategoryAdmin(ModelAdmin):
    model = MemberCategory
    menu_label = "Member Categories"


class ProjectCategoryAdmin(ModelAdmin):
    model = ProjectCategory
    menu_label = "Project Categories"


class CategoryModelAdminGroup(ModelAdminGroup):
    menu_label = "Categories"
    menu_icon = "folder-open-inverse"
    menu_order = 400
    items = (MemberCategoryAdmin, ProjectCategoryAdmin)


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
    list_filter = ("category", "tags")
    search_fields = ("title", "intro", "description")

class ContentAdminModel(ModelAdminGroup):
    menu_label = "Content"
    menu_icon = "folder-open-inverse"
    menu_order = 300
    items = (ProjectModelAdmin,)

class PublicationModelAdmin(ModelAdmin):
    model = Publication
    menu_label = "Publications"
    list_display = ("title", "date", "link_to_publication", "type_of_publication")
    search_fields = ("title", "date")


class PatentModelAdmin(ModelAdmin):
    model = Patent
    menu_label = "Patents"
    list_display = ("title", "date", "link_to_publication", "type_of_patent")
    list_filter = ("type_of_patent",)
    search_fields = ("title", "date")


class ResearchModelAdminGroup(ModelAdminGroup):
    menu_label = "Research"
    menu_icon = "folder-open-inverse"
    menu_order = 400
    items = (PublicationModelAdmin, PatentModelAdmin)


modeladmin_register(CategoryModelAdminGroup)
modeladmin_register(TeamAdminModel)
modeladmin_register(ContentAdminModel)
modeladmin_register(ResearchModelAdminGroup)
    