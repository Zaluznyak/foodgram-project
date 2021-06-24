from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('ingredients', views.IngredientsApiView)
router.register('favorites', views.FavoritesApiView)
router.register('subscriptions', views.FollowApiView)
router.register('shoplists', views.ShopListApiView)


urlpatterns = [
    path('v1/', include(router.urls)),
]
