from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.viewsets import ModelViewSet
from polls.models import ClothingType, Company, CompanyModel, Size, User, UserModel
from polls.serializers import ClothingTypeSerializer, CompanyModelSerializer, CompanySerializer, SizeSerializer, UserModelSerializer, UserSerializer

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

class UserViewSet(ModelViewSet):
      serializer_class = UserSerializer
      queryset = User.objects.all()

class UserModelViewSet(ModelViewSet):
      serializer_class = UserModelSerializer
      queryset = UserModel.objects.all()

class CompanyViewSet(ModelViewSet):
      serializer_class = CompanySerializer
      queryset = Company.objects.all()

class CompanyModelViewSet(ModelViewSet):
      serializer_class = CompanyModelSerializer
      queryset = CompanyModel.objects.all()


class SizeViewSet(ModelViewSet):
      serializer_class = SizeSerializer
      queryset = Size.objects.all()


class ClothingTypeViewSet(ModelViewSet):
      serializer_class = ClothingTypeSerializer
      queryset = ClothingType.objects.all()
