from django.conf.urls import include, url
from django.urls import path
from rest_framework.routers import DefaultRouter
from mapps.users.views import *
from mapps.data.views import *


router = DefaultRouter()

router.register(r'aboutus', AboutUsViewSet)
router.register(r'team', TeamViewSet)
router.register(r'descriptions', PhysicalDescriptionViewSet)
router.register(r'cases', CaseViewSet)
router.register(r'sightings', SightingViewSet)
router.register(r'privacy', PrivacyPolicyViewSet)
router.register(r'users', UserViewSet)
router.register(r'faq', FAQViewSet)



urlpatterns = [
     url(r'^cases/recents(?P<id>.+)$', CaseLatest.as_view()),
     url(r'^cases/search(?P<query>.+)$', CaseSearch.as_view()),
     url(r'^users/login/$', login_user),
     url(r'^users/me/$', CurrentUserProfile.as_view()),
     url(r'^', include(router.urls)),
]