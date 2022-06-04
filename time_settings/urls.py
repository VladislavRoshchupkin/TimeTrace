from django.contrib import admin
from django.urls import path, include
from app.views.views import *
from app.views.api_views import *
from rest_framework import permissions
import notifications.urls
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="TimeTrace API",
      default_version='v1',
      description="TimeTrace swagger",
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.urls')),
    path('api/', include('rest_framework.urls')),
    path('api/project', ProjectList.as_view()),
    path('api/time', TimeList.as_view()),
    path('api/task', TaskList.as_view()),
    path('api/department', DepartmentList.as_view()),
    path('api/raiting', RaitingList.as_view()),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('notifications/', include(notifications.urls, 
    namespace='notifications')),
]
