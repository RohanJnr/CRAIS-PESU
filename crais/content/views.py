from django.http import Http404
from django.views.generic import DetailView, ListView
from django.db.models import QuerySet

from crais.content.models import Member, Patent, Publication


class PublicationsView(ListView):
    """ListView generic for Publication model."""

    model = Publication

    def get_context_data(self, *, object_list: list | None = None, **kwargs) -> dict:
        """Modify context to include publication years."""
        context = super().get_context_data(object_list=object_list, **kwargs)

        publication_years = Publication.objects.dates('date', 'year')
        context["publication_years"] = [date.year for date in publication_years]

        return context


class PatentsView(ListView):
    """ListView generic for Patents model."""

    model = Patent

    def get_context_data(self, *, object_list: list | None = None, **kwargs) -> dict:
        """Modify context to include patent filed years."""
        context = super().get_context_data(object_list=object_list, **kwargs)

        filed_years = Patent.objects.dates('date_filed', 'year')
        context["filed_years"] = [date.year for date in filed_years]

        return context


class MemberView(DetailView):
    """DetailView generic for Member model."""

    model = Member
    query_pk_and_slug = True

    def get_object(self, queryset: QuerySet | None = None) -> Member:
        """Override get_object to return http404 on members without a page."""
        obj:Member = super().get_object(queryset)
        if not obj.member_page:
            return Http404("Detail page not found for member.")
        return obj
