from django.contrib import admin
from django.urls import path, include
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from products.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('catalogs/', include('catalogs.urls')),
    path('brands/', include('brands.urls')),
    path('colors/', include('colors.urls')),
    path('products/', include('products.urls')),
    path('', home, name='home'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)