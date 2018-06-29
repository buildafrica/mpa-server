# from django.conf import settings
from django.urls import path, include, re_path
from django.conf.urls import  url, include
from rest_framework import routers
from rest_framework_swagger.views import get_swagger_view
from home.views import *
from users.views import *
from rest_framework.authtoken.views import obtain_auth_token

router = routers.DefaultRouter()
router.register('users', UserViewSet)
router.register('sightings', SightingViewSet)
router.register('faq', FAQViewSet)
router.register('cases', CaseViewSet)
router.register('aboutus', AboutUsViewSet)
router.register('team', TeamViewSet) 
router.register('privacypolicy', PrivacyPolicyViewSet)

schema_view = get_swagger_view(title='Pastebin API')

urlpatterns = [
    path('docs/', schema_view),
    path('', include(router.urls)),
    re_path('users/me/', CurrentUserProfile.as_view()),
    re_path('users/social-signup/', UserSocialSignUp.as_view()),
    re_path('users/get-auth-token/', obtain_auth_token, name='api-token'),
]
