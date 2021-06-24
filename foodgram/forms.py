from django import forms
from django.core.exceptions import ValidationError

from .models import Ingredients, Recipe, Tag
from .func import add_ingredients


class RecipeForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        label="Теги",
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
    ingredients = forms.CharField(
        required=False,
        label="Ингредиенты",
        widget=forms.TextInput(attrs={"id": "nameIngredient"}),
    )

    class Meta:
        model = Recipe
        fields = ("name", "tags", "ingredients", "time", "text", "image",)
        labels = {
            "name": "Название рецепта",
            "text": "Описание",
            "time": "Время приготовления",
            "image": "Фото",
        }
        widgets = {
            "time": forms.TextInput(),
        }

    def clean_ingredients(self):
        ingredients = list(
            zip(self.data.getlist("nameIngredient"),
                self.data.getlist("valueIngredient"),),
        )
        if not ingredients:
            raise forms.ValidationError("Отсутствуют ингредиенты")
        all = Ingredients.objects.all()
        ingredients_clean = []
        for name, quantity in ingredients:
            if not all.filter(name=name):
                raise ValidationError(
                    f'В базе данных нет "{name}".'
                    )
            if int(quantity) < 1:
                raise forms.ValidationError(
                    f'Неверное кол-во ингредиента "{name}".'
                    )
            else:
                ingredients_clean.append(
                    {
                        "name": name,
                        "quantity": quantity,
                    }
                )
        return ingredients_clean

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.save()
        ingredients = self.cleaned_data["ingredients"]
        self.cleaned_data["ingredients"] = []
        self.save_m2m()
        add_ingredients(self.instance, ingredients)
        return instance
