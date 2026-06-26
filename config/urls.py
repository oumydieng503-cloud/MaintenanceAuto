from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from garage.views import (
    page_login,
    page_register,
    page_dashboard_client,
    page_dashboard_mecanicien,
    page_dashboard_admin,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('garage.urls')),
    # Documentation automatique
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    #urls frontend
    path('', page_login, name='login'),
    path('inscription/', page_register, name='register'),
    path('dashboard/client/', page_dashboard_client, name='dashboard-client'),
    path('dashboard/mecanicien/', page_dashboard_mecanicien, name='dashboard-mecanicien'),
    path('dashboard/admin/', page_dashboard_admin, name='dashboard-admin'),
]