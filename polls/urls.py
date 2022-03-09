from django.conf.urls import include, re_path
from rest_framework.routers import DefaultRouter

from polls.models import ClothingType, Company, CompanyModel, Size, User, UserModel
from .views import ClothingTypeViewSet, CompanyModelViewSet, CompanyViewSet, SizeViewSet, UserModelViewSet, UserViewSet

from . import views

router = DefaultRouter()
router.register(User, UserViewSet, base_name='user')
router.register(UserModel, UserModelViewSet, base_name='user-model')
router.register(Company, CompanyViewSet, base_name='company')
router.register(CompanyModel, CompanyModelViewSet, base_name='company-model')
router.register(Size, SizeViewSet, base_name='size')
router.register(ClothingType, ClothingTypeViewSet, base_name='clothing-type')


urlpatterns = [
    re_path('', views.index, name='index'),
]