from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls")),
    path("items/", include("item.urls")),
    path("dashboard/", include("dashboard.urls")),
    path("inbox/", include("communication.urls")),
    path("accounts/", include("allauth.urls")),
    path("", include("cart.urls")),
    path("paypal", include("paypal.standard.ipn.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
