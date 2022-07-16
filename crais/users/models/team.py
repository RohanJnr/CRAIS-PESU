from django.db import models
from modelcluster.models import ClusterableModel
from wagtail.search import index
from wagtail.snippets.models import register_snippet


@register_snippet
class Member(index.Indexed, ClusterableModel):
    name = models.CharField(max_length=255)

    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    def __str__(self) -> str:
        return self.name