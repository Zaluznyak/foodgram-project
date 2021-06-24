from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class TagChoices(models.TextChoices):
    BREAKFAST = "breakfast", "Завтрак"
    LUNCH = "lunch", "Обед"
    DINNER = "dinner", "Ужин"


class ColorChoices(models.TextChoices):
    GREEN = "green", "Зеленый"
    ORANGE = "orange", "Оранжевый"
    PURPLE = "purple", "Фиолетовый"


class Tag(models.Model):
    ingestion = models.CharField(choices=TagChoices.choices,
                                 default=TagChoices.LUNCH, unique=True,
                                 max_length=10, verbose_name='Время приема')
    color = models.CharField(choices=ColorChoices.choices,
                             default=ColorChoices.GREEN, unique=True,
                             max_length=10, verbose_name='Цвет')

    def __str__(self):
        return self.ingestion


class Ingredients(models.Model):
    name = models.CharField(verbose_name='Наименование',
                            max_length=100)
    dimension = models.CharField(verbose_name='Единица измерения',
                                 max_length=40)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['name', 'dimension'],
                                               name='unique_ingredients')]

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='recipes', verbose_name='Автор')
    name = models.CharField('Название', max_length=150)
    image = models.ImageField(
        'Картинка', upload_to='recipes/',
        blank=True, null=True
    )
    text = models.TextField('Описание')
    time = models.PositiveSmallIntegerField('Время приготовления',
                                            help_text='В минутах')
    tags = models.ManyToManyField(Tag, blank=True, related_name='recipes',
                                  verbose_name='Тег')
    ingredients = models.ManyToManyField(Ingredients,
                                         through='RecipeIngredient',
                                         verbose_name='Ингредиенты')
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True,
                                    db_index=True)

    class Meta:
        ordering = ["-pub_date"]

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    ingredient = models.ForeignKey(Ingredients, on_delete=models.CASCADE,
                                   verbose_name='Ингридиент')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               verbose_name='Рецепт',
                               related_name='recipe_ingredient')
    quantity = models.PositiveSmallIntegerField('Количество')

    def __str__(self):
        return self.ingredient.name


class Favorites(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='Favorites',
                             verbose_name='Пользователь')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='Favorites_recipes')

    class Meta:
        constraints = [models.UniqueConstraint(fields=['user', 'recipe'],
                                               name='unique_favorites')]

    def __str__(self):
        return self.recipe.name


class ShopList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='shoplist',
                             verbose_name='Пользователь')

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='in_shoplist',
                               verbose_name='Рецепт')

    class Meta:
        constraints = [models.UniqueConstraint(fields=['user', 'recipe'],
                                               name='unique_list')]

    def __str__(self):
        return self.recipe.name
