from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('jet/', include('jet.urls', 'jet')),
    path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),  # Django JET dashboard URLS
    path('admin/', admin.site.urls),
    path('',include('ad_app.urls')),
    path('api/',include('insert_app.urls'))
]

if settings.DEBUG:
    urlpatterns += [
        *static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
    ]