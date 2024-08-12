from django.contrib import admin
from django.urls import path, include
from accounts.views import entry
from products.views import dashboard
from django.conf.urls.static import static
from django.conf import settings
from accounts.views import google_authenticate, google_callback, activate

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin_tools_stats/', include('admin_tools_stats.urls')),
    path('entry/', entry, name='entry'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('dashboard/', dashboard, name='dashboard'),
    path('google_authenticate/', google_authenticate, name='google_authenticate'),
    path('google_callback/', google_callback, name='google_callback'),
]

admin.site.index_title="TrackIt"
admin.site.site_header="TrackIt Admin Dashboard"
admin.site.site_title="Admin Dashboard"

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)