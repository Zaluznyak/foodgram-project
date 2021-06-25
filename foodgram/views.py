import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Exists, OuterRef
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)
from django_filters.views import BaseFilterView

from final_project import settings
from .filters import TagRecipeFilterSet
from .forms import RecipeForm
from .mixins import TagMixin
from .models import Favorites, ShopList, Recipe
from .permissions import IsAuthorOrAdminOrReadOnly
from .func import shoplist_ingredients

User = get_user_model()


class IndexView(TagMixin, BaseFilterView, ListView):
    model = Recipe
    template_name = 'index.html'
    paginate_by = settings.PAGE
    filterset_class = TagRecipeFilterSet

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_authenticated:
            return queryset
        user = self.request.user
        queryset = queryset.annotate(is_favorited=Exists(
            Favorites.objects.filter(
                user=user,
                recipe=OuterRef('pk'),),
                ),).annotate(is_shop_list=Exists(
                    ShopList.objects.filter(
                        user=user,
                        recipe=OuterRef('pk'),),),)
        return queryset


class FavoriteView(TagMixin, LoginRequiredMixin,
                   BaseFilterView, ListView):
    model = Recipe
    template_name = 'favorite.html'
    paginate_by = settings.PAGE
    filterset_class = TagRecipeFilterSet
    queryset = Recipe.objects.all()

    def get_queryset(self):
        return FavoriteView.queryset.filter(
            Favorites_recipes__user=self.request.user)


class FollowView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'myFollow.html'
    paginate_by = settings.PAGE
    queryset = User.objects.all()

    def get_queryset(self):
        return FollowView.queryset.filter(
            following__user=self.request.user).order_by('-id')


class ProfileView(TagMixin, BaseFilterView, ListView):
    model = Recipe
    template_name = 'authorRecipe.html'
    paginate_by = settings.PAGE
    filterset_class = TagRecipeFilterSet
    queryset = Recipe.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        author = get_object_or_404(User, username=self.kwargs['username'])
        is_follower = False
        if self.request.user.is_authenticated:
            is_follower = self.request.user.following.filter(
                author=author).exists()
        context.update(
            {
                'user_is_follower': is_follower,
                'author': author,
            }
        )
        return context

    def get_queryset(self):
        author = get_object_or_404(User, username=self.kwargs['username'])
        return ProfileView.queryset.filter(author=author)


class RecipeView(DetailView):
    model = Recipe
    template_name = 'singlePage.html'


class RecipeUpdateView(LoginRequiredMixin, UpdateView):
    model = Recipe
    permission_classes = IsAuthorOrAdminOrReadOnly
    template_name = 'formRecipe.html'
    form_class = RecipeForm
    success_url = reverse_lazy('foodgram:index')


class RecipeDeleteView(LoginRequiredMixin, DeleteView):
    model = Recipe
    template_name = 'confirm_delete.html'
    permission_classes = IsAuthorOrAdminOrReadOnly
    success_url = reverse_lazy('foodgram:index')


class RecipeCreateView(LoginRequiredMixin, CreateView):
    model = Recipe
    template_name = 'formRecipe.html'
    form_class = RecipeForm
    success_url = reverse_lazy('foodgram:index')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ShopListView(LoginRequiredMixin, ListView):
    model = Recipe
    template_name = 'shopList.html'
    queryset = Recipe.objects.all()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['object_list'] = self.get_user_purchase()
        return context

    def get_user_purchase(self):
        return ShopListView.queryset.filter(
            in_shoplist__user=self.request.user)


@login_required
def shoplist_download(request):
    now = datetime.datetime.now()
    date = now.strftime('%d-%m-%Y')
    result = shoplist_ingredients(request.user)
    response = HttpResponse(result, content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename = {date}.txt'
    return response


def page_not_found(request, exception=None):
    return render(request, 'misc/404.html', {'path': request.path}, status=404)


def server_error(request):
    return render(request, 'misc/500.html', status=500)
