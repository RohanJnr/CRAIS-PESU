from typing import Any

from django.contrib import messages
from django.http import Http404, HttpRequest
from django.shortcuts import redirect
from django.views.generic import DetailView, ListView, RedirectView, View
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


class MemberView(View):
    """DetailView generic for Member model."""

    def get(self, request: HttpRequest, *args, **kwargs) -> str | None:
        slug = kwargs.get("slug")
        try:
            member = Member.objects.get(slug=slug)
        except Member.DoesNotExist:
            return redirect("/team")

        if member.pes_faculty_profile_link:
            return redirect(member.pes_faculty_profile_link)
        
        return redirect("/team")