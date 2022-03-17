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
                  return Response({"Failure": "Wrong syntax for dimensions field : Control Object or Dimensions for the User model is missing !"}, status=status.HTTP_400_BAD_REQUEST)
            controlobject = array[0].split(',')
            if len(controlobject) != 5:
                  return Response({"Failure": "Wrong syntax for dimensions field : Control Object field is missing some information"}, status=status.HTTP_400_BAD_REQUEST)
            keypoints = array[1].split(',')
            if (len(keypoints) <= 4) | (len(keypoints) % 4 != 0):
                  return Response({"Failure": "Wrong syntax for dimensions field : Dimensions for the User Model field is missing some information"}, status=status.HTTP_400_BAD_REQUEST)

            arr_control = [float(i) for i in controlobject]
            arr_keypoints = [float(j) for j in keypoints]

            scale = arr_control[4] / sqrt((arr_control[0] - arr_control[2])**2 + (arr_control[1] - arr_control[3])**2)
            arr_final = []
            for x in range(0, len(arr_keypoints), 4):
                  dim = scale * sqrt((arr_keypoints[x] - arr_keypoints[x+2])**2 + (arr_keypoints[x+1] - arr_keypoints[x+3])**2) 
                  arr_final.append(dim)
            string = ""
            for x in range(len(arr_final) - 1):
                  string = string + str(arr_final[x]) + ","
            string = string + str(arr_final[len(arr_final) - 1])
            request.query_params._mutable = True
            request.data['dimensions'] = string
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
