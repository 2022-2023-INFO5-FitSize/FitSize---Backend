# serializers.py
from rest_framework.serializers import ModelSerializer

from .models import ClothingType, Company, CompanyModel, Size, User, UserModel

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'login', 'password')

class UserModelSerializer(ModelSerializer):
    class Meta:
        model = UserModel
        fields = ('id', 'name', 'dimensions', 'user', 'clothingtype')

class CompanySerializer(ModelSerializer):
    class Meta:
        model = Company
        fields = ('id', 'name', 'adress')

class CompanyModelSerializer(ModelSerializer):
    class Meta:
        model = CompanyModel
        fields = ('id', 'color', 'dimensions', 'company', 'size', 'clothingtype')

class SizeSerializer(ModelSerializer):
    class Meta:
        model = Size
        fields = ('id', 'label', 'origin')

class ClothingTypeSerializer(ModelSerializer):
    class Meta:
        model = ClothingType
        fields = ('id', 'label', 'points')


