from django.urls import include, re_path
from rest_framework import routers

from polls.views import UserViewSet

# from . import views

router = routers.SimpleRouter()
router.register(r'users', UserViewSet)
# router.register(r'user-model', UserModelViewSet)
# router.register(r'company', CompanyViewSet)
# router.register(r'company-model', CompanyModelViewSet)
# router.register(r'size', SizeViewSet)
# router.register(r'clothing-type', ClothingTypeViewSet)

urlpatterns = [
    re_path('^', include(router.urls)),
]