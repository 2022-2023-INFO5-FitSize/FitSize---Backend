from django.urls import include, re_path
from rest_framework import routers
from polls.views import UserViewSet, UserModelViewSet, CompanyViewSet, CompanyModelViewSet, SizeViewSet, ClothingTypeViewSet

router = routers.SimpleRouter()
router.register(r'user', UserViewSet)
router.register(r'usermodel', UserModelViewSet)
router.register(r'company', CompanyViewSet)
router.register(r'companymodel', CompanyModelViewSet)
router.register(r'size', SizeViewSet)
router.register(r'clothingtype', ClothingTypeViewSet)

urlpatterns = [
    re_path('^', include(router.urls)),
]