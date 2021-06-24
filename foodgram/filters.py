from django_filters import FilterSet
from django_filters.filters import ModelMultipleChoiceFilter

from .models import Recipe, Tag


class TagRecipeFilterSet(FilterSet):
    tags = ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(),
        field_name='tags__ingestion',
        to_field_name='ingestion',
    )

    class Meta:
        model = Recipe
        fields = ('tags',)
