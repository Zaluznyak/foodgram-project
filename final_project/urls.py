from django.contrib import admin
from django.urls import include, path
from django.conf.urls import handler404, handler500
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.flatpages import views

from foodgram import views as foodgram_views

handler404 = "foodgram.views.page_not_found" # noqa
handler500 = "foodgram.views.server_error" # noqa

urlpatterns = [
    path("404/", foodgram_views.page_not_found, name="404"),
    path("500/", foodgram_views.server_error, name="500"),
    path("admin/", admin.site.urls),
    path("auth/", include("users.urls")),
    path("auth/", include("django.contrib.auth.urls")),
    path("about/", include("django.contrib.flatpages.urls")),
    path(
            "about-author/", views.flatpage,
            {"url": "/about-author/"}, name="about"
            ),
    path(
            "about-spec/", views.flatpage,
            {"url": "/about-spec/"}, name="spec"
            ),
    path("api/", include("api.urls")),
    path("", include("foodgram.urls"))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT
                          )
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT
                          )
