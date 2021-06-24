import types

from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, viewsets
from rest_framework.response import Response

from foodgram.models import Favorites, Ingredients, ShopList
from users.models import Follow

from . import serializers

SUCCESS = types.MappingProxyType({'success': True})
UNSUCCESS = types.MappingProxyType({'success': False})


class BaseInstanceView(mixins.CreateModelMixin,
                       mixins.DestroyModelMixin,
                       viewsets.GenericViewSet):

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(SUCCESS)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        is_deleted = instance.delete()
        if is_deleted:
            return Response(SUCCESS)
        return Response(UNSUCCESS)


class FavoritesApiView(BaseInstanceView):
    queryset = Favorites.objects.all()
    serializer_class = serializers.FavoritesSerializer

    def get_object(self):
        instance = get_object_or_404(
            Favorites,
            user=self.request.user,
            recipe=self.kwargs['pk'],
        )
        return instance


class IngredientsApiView(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Ingredients.objects.all()
    serializer_class = serializers.IngredientsSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ('name',)


class FollowApiView(BaseInstanceView):
    queryset = Follow.objects.all()
    serializer_class = serializers.FollowSerializer

    def get_object(self):
        instance = get_object_or_404(
            FollowApiView.queryset,
            user=self.request.user,
            author=self.kwargs['pk'],
        )
        self.check_object_permissions(self.request, instance)
        return instance


class ShopListApiView(mixins.ListModelMixin, BaseInstanceView):
    queryset = ShopList.objects.all()
    serializer_class = serializers.ShopListSerializer

    def get_object(self):
        instance = get_object_or_404(
            ShopListApiView.queryset,
            user=self.request.user,
            recipe=self.kwargs['pk'],
        )
        self.check_object_permissions(self.request, instance)
        return instance
