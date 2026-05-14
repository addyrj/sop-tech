from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView
from django.db import connection  # 👈 important
from .settings import BASE_DIR
# Change the admin site header






urlpatterns = [
    path('', RedirectView.as_view(url='/admin/', permanent=False)),  # Redirect root to /admin/
    path('admin/', admin.site.urls),
    path('sop/', include('sop.urls')),
    path('api/', include('sop.api.urls')),
]


from django.views.static import serve
from django.urls import re_path

# Serve media files in development
if settings.DEBUG:
    urlpatterns += [
        re_path(r'^upload/(?P<path>.*)$', serve, {'document_root': BASE_DIR / 'upload'}),
        re_path(r'^tvfile/(?P<path>.*)$', serve, {'document_root': BASE_DIR / 'tvfile'}),
    ]
