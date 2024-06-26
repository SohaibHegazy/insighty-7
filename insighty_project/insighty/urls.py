from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('plot/', views.plot, name='plot'),
    path('refresh/', views.refresh, name='refresh'),
    path('delete/', views.delete_file, name='delete_file'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)