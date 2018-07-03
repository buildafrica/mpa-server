from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url
from django.conf import settings
from rest_framework_swagger.views import get_swagger_view
from rest_framework.documentation import include_docs_urls

schema_view = get_swagger_view(title='Missing Persons Project API')

urlpatterns = [
    # url('grappelli/', include('grappelli.urls')), # grappelli URLS
    url('admin/', admin.site.urls),
    # url(r'^', include('mapps.data.urls')),
    url(r'^api/v1.0/', include(('mapps.rest.urls', 'mapps.rest'), namespace='api')),
    # url(r'^document/', include_docs_urls(title='Missing Persons Project API', public=False,)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^docs/', schema_view),
]

