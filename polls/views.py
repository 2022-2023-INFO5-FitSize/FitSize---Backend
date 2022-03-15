from asyncio.windows_events import NULL
from math import sqrt
from rest_framework.decorators import action
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.viewsets import ModelViewSet
from polls.models import ClothingType, Company, CompanyModel, Size, User, UserModel
from polls.serializers import ClothingTypeSerializer, CompanyModelSerializer, CompanySerializer, SizeSerializer, UserModelSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework import status
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

class UserViewSet(ModelViewSet):
      serializer_class = UserSerializer
      queryset = User.objects.all()

class UserModelViewSet(ModelViewSet):
      serializer_class = UserModelSerializer
      queryset = UserModel.objects.all()

      @action(methods=['post'])
      def saveFromKeyPoints(self, request, *args, **kwargs) :
            userModels = UserModel.objects.all()
            data = request.data
            keypoints = data.keypoints
            controlobject = data.control.object
            scale = controlobject.length / sqrt((controlobject.point1.x - controlobject.point2.x)**2 + (controlobject.point1.y - controlobject.point2.y)**2)
            dim1 = scale * sqrt((keypoints.point1.x - keypoints.point2.x)**2 + (keypoints.point1.y - keypoints.point2.y)**2)
            dim2 = scale * sqrt((keypoints.point3.x - keypoints.point4.x)**2 + (keypoints.point3.y - keypoints.point4.y)**2)
            dim3 = scale * sqrt((keypoints.point5.x - keypoints.point6.x)**2 + (keypoints.point5.y - keypoints.point6.y)**2)
            serializer = UserModelSerializer(userModels, name=data.name, dimensions=[dim1,dim2,dim3])
            if serializer.is_valid :
                  serializer.save()
                  return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
