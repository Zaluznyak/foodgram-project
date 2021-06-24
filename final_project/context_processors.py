def shop_list_count(request):
    if request.user.is_authenticated:
        count = request.user.shoplist.all().count()
    else:
        count = 0
    return {
        "shop_list_count": count
    }
