
from django import template
from django.contrib.auth import get_user_model

from ..models import Favorites, ShopList
from users.models import Follow


register = template.Library()
User = get_user_model()


@register.filter
def is_shop_list(recipe, user):
    return ShopList.objects.filter(recipe=recipe, user=user).exists()


@register.filter
def is_favorited(recipe, user):
    return Favorites.objects.filter(recipe=recipe, user=user).exists()


@register.filter
def is_follower(user, author):
    return Follow.objects.filter(author=author, user=user).exists()


@register.simple_tag(takes_context=True)
def manage_tags(context, **kwargs):
    tag = kwargs["tag"]
    query_string = context["request"].GET.copy()
    tags = query_string.getlist("tags")
    if tag in tags:
        tags.remove(tag)
    else:
        tags.append(tag)
    query_string.setlist("tags", tags)

    if "page" in query_string:
        query_string.pop("page")

    return query_string.urlencode()


@register.filter
def tags_to_url_params(tags):
    url_param_tags = [f'tag={tag}' for tag in tags]
    return '&' + '&'.join(url_param_tags)
