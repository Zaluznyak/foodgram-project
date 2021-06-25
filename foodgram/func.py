import datetime

from django.db.models import Sum
from django.shortcuts import get_object_or_404

from .models import Ingredients, Recipe, RecipeIngredient


def add_ingredients(recipe, ingredients):
    Recipe.ingredients.through.objects.bulk_create(
        [Recipe.ingredients.through(recipe=recipe,
                                    ingredient=get_object_or_404(
                                        Ingredients,
                                        name=ingredient["name"],
                                        ),
                                    quantity=ingredient["quantity"],
                                    ) for ingredient in ingredients],
    )


def shoplist_ingredients(request_user):
    ingredients = (
        RecipeIngredient.objects.filter(
            recipe__in_shoplist__user=request_user,
        ).values("ingredient__name", "ingredient__dimension",).annotate(
            quantity=Sum("quantity")
            )
    )
    now = datetime.datetime.now()
    date = now.strftime("%d-%m-%Y %H:%M")
    download_list = [f"~~~ Список покупок ~~~ \r\n {date} \r\n"]
    for ingredient in ingredients:
        download_list.append(
            f'{ingredient["ingredient__name"]} '
            f'{ingredient["quantity"]} '
            f'{ingredient["ingredient__dimension"]};\r\n')
    return download_list
