from django.conf import settings
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.contrib.auth.views import password_reset_done, password_reset_confirm, password_reset_complete


urlpatterns = [
    path('jet/', include('jet.urls', 'jet')),
    path('jet/dashboard', include('jet.dashboard.urls', 'jet-dashboard')),
    path('admin/', admin.site.urls),
    path('', include('rest.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_frameworks')),
    re_path('resetpassword/passwordsent/$', password_reset_done, name='password_reset_done'),
   re_path('reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', password_reset_confirm, name='password_reset_confirm'),
   re_path('reset/done/$', password_reset_complete, name='password_reset_complete'),
   re_path('direct/$', TemplateView.as_view, {'template': 'direct.html','extra_context':{'showDirect':True}}),
    # re_path(r'^docs/', include('rest_framework_swagger.urls')),
    # re_path(r'^api/', include('djoser.urls')),
    # re_path(r'^api/', include('djoser.urls.jwt')),
]
