from asyncio.windows_events import NULL
from math import sqrt
from rest_framework.decorators import action
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

      @action(methods=['post'], detail=False, url_path='savedimensions',url_name="Save dimensions")
      def saveFromKeyPoints(self, request, *args, **kwargs) :
            array = request.data['dimensions']
            array = array.split('KP')
            if len(array) != 2:
                  return Response({"Failure": "Wrong syntax for dimensions field"}, status=status.HTTP_400_BAD_REQUEST)
            keypoints = array[1].split(',')
            controlobject = array[0].split(',')

            arr_control = [float(i) for i in controlobject]
            arr_keypoints = [float(j) for j in keypoints]

            # scale = controlobject.length / sqrt((controlobject.point1.x - controlobject.point2.x)**2 + (controlobject.point1.y - controlobject.point2.y)**2)
            # dim1 = scale * sqrt((keypoints.point1.x - keypoints.point2.x)**2 + (keypoints.point1.y - keypoints.point2.y)**2)
            # dim2 = scale * sqrt((keypoints.point3.x - keypoints.point4.x)**2 + (keypoints.point3.y - keypoints.point4.y)**2)
            # dim3 = scale * sqrt((keypoints.point5.x - keypoints.point6.x)**2 + (keypoints.point5.y - keypoints.point6.y)**2)

            scale = float(len(arr_control)) / sqrt((arr_control[0] - arr_control[2])**2 + (arr_control[1] - arr_control[3])**2)
            dim1 = scale * sqrt((arr_keypoints[0] - arr_keypoints[2])**2 + (arr_keypoints[1] - arr_keypoints[3])**2)
            dim2 = scale * sqrt((arr_keypoints[4] - arr_keypoints[6])**2 + (arr_keypoints[5] - arr_keypoints[7])**2)
            dim3 = scale * sqrt((arr_keypoints[8] - arr_keypoints[10])**2 + (arr_keypoints[9] - arr_keypoints[11])**2)

            request.data['dimensions'] = str(dim1) + "," + str(dim2) + "," + str(dim3)
            #return Response(request.data, status=status.HTTP_201_CREATED)
            return self.create(request, *args, **kwargs)

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
