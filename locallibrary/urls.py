from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', RedirectView.as_view(url='/catalog/', permanent=True)),
    path('admin/', admin.site.urls),
    path('catalog/', include('catalog.urls')),
    path('social/', include('social_django.urls', namespace="social")),
    path('accounts/', include('django.contrib.auth.urls')),
    path('blog/', include('blog.urls')),
    path('__debug__/', include('debug_toolbar.toolbar')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_URL)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
