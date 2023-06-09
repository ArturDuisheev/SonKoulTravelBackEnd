from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin

schema_view = get_schema_view(
   openapi.Info(
      title="SonKoulTravel API",
      default_version='v1',
      description="Description of SonKoulTravel API",
      terms_of_service="https://www.example.com/terms/",
      contact=openapi.Contact(email="myworkingartur@gmail.com"),
      license=openapi.License(name="POfse License"),
   ),
   public=True,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('main_page/', include('main_page.urls')),
    path('actions/', include('client_actions.urls')),
    path('tour/', include('tour.urls')),
    path('blog/', include('blog_and_news.urls')),
    path('car/', include('transport.urls')),
    path('summernote/', include('django_summernote.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
