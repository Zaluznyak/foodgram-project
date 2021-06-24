from django.urls import path

from . import views

app_name = 'foodgram'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('new/', views.RecipeCreateView.as_view(), name='new'),
    path('follow/', views.FollowView.as_view(), name='follow'),
    path('favorites/', views.FavoriteView.as_view(), name='favorites'),
    path('shoplists/', views.ShopListView.as_view(), name='shoplist'),
    path(
        'shoplists/download/',
        views.shoplist_download,
        name='get_shoplist',
    ),
    path('<str:username>/', views.ProfileView.as_view(), name='profile'),
    path(
        '<str:username>/<int:pk>/',
        views.RecipeView.as_view(),
        name='recipe',
    ),
    path(
        '<str:username>/<int:pk>/edit/',
        views.RecipeUpdateView.as_view(),
        name='recipe_edit',
    ),
    path(
        '<str:username>/<int:pk>/delete/',
        views.RecipeDeleteView.as_view(),
        name='recipe_delete',
    )
]
