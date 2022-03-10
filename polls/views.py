from django.shortcuts import render
from django.http import HttpResponse

from rest_framework.mixins import (
    CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin
)
from rest_framework.viewsets import GenericViewSet

from .models import ClothingType, Company, CompanyModel, Size, User, UserModel
from .serializers import ClothingTypeSerializer, CompanyModelSerializer, CompanySerializer, SizeSerializer, UserModelSerializer, UserSerializer


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

class UserViewSet(GenericViewSet,  # generic view functionality
                     CreateModelMixin,  # handles POSTs
                     RetrieveModelMixin,  # handles GETs for 1 User
                     UpdateModelMixin,  # handles PUTs and PATCHes
                     ListModelMixin):  # handles GETs for many Users
      serializer_class = UserSerializer
      queryset = User.objects.all()

class UserModelViewSet(GenericViewSet,
                     CreateModelMixin,
                     RetrieveModelMixin,
                     UpdateModelMixin,
                     ListModelMixin):
      serializer_class = UserModelSerializer
      queryset = UserModel.objects.all()

class CompanyViewSet(GenericViewSet,
                     CreateModelMixin,
                     RetrieveModelMixin,
                     UpdateModelMixin,
                     ListModelMixin):
      serializer_class = CompanySerializer
      queryset = Company.objects.all()

class CompanyModelViewSet(GenericViewSet,
                     CreateModelMixin,
                     RetrieveModelMixin,
                     UpdateModelMixin,
                     ListModelMixin):
      serializer_class = CompanyModelSerializer
      queryset = CompanyModel.objects.all()


class SizeViewSet(GenericViewSet,
                     CreateModelMixin,
                     RetrieveModelMixin,
                     UpdateModelMixin,
                     ListModelMixin):
      serializer_class = SizeSerializer
      queryset = Size.objects.all()


class ClothingTypeViewSet(GenericViewSet,
                     CreateModelMixin,
                     RetrieveModelMixin,
                     UpdateModelMixin,
                     ListModelMixin):
      serializer_class = ClothingType
      queryset = ClothingType.objects.all()
