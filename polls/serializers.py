# serializers.py
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import ClothingType, Company, CompanyModel, Size, User, UserModel
from .models import User

class UserSerializer(ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(required=True,
                                            allow_null=False,
                                            queryset=User.objects.all())
    class Meta:
        model = User
        fields = ('id', 'login', 'password')

class ClothingTypeSerializer(ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(required=True,
                                            allow_null=False,
                                            queryset=User.objects.all())
    class Meta:
        model = ClothingType
        fields = ('id', 'label', 'points')

class UserModelSerializer(ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(required=True,
                                            allow_null=False,
                                            queryset=User.objects.all())
    user = UserSerializer(read_only=True)
    clothingtype = ClothingTypeSerializer(read_only=True)
    class Meta:
        model = UserModel
        fields = ('id', 'name', 'dimensions', 'user', 'clothingtype')

class CompanySerializer(ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(required=True,
                                            allow_null=False,
                                            queryset=User.objects.all())
    class Meta:
        model = Company
        fields = ('id', 'name', 'adress')
    
class SizeSerializer(ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(required=True,
                                            allow_null=False,
                                            queryset=User.objects.all())
    class Meta:
        model = Size
        fields = ('id', 'label', 'origin')

class CompanyModelSerializer(ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(required=True,
                                            allow_null=False,
                                            queryset=User.objects.all())
    size = SizeSerializer(read_only=True)
    company = CompanySerializer(read_only=True)
    clothingtype = ClothingTypeSerializer(read_only=True)
    class Meta:
        model = CompanyModel
        fields = ('id', 'color', 'dimensions', 'company', 'size', 'clothingtype')


