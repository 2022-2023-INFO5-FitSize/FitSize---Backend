from rest_framework.serializers import ModelSerializer

from polls.models import ClothingType, Company, CompanyModel, Size, User, UserModel


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'login', 'password')


class ClothingTypeSerializer(ModelSerializer):
    class Meta:
        model = ClothingType
        fields = ('id', 'label', 'points')


class UserModelSerializer(ModelSerializer):

    class Meta:
        model = UserModel
        fields = ('id', 'name', 'dimensions', 'user', 'clothingtype')

    def to_representation(self, instance):
        self.fields['user'] = UserSerializer(read_only=True)
        self.fields['clothingtype'] = ClothingTypeSerializer(read_only=True)
        return super(UserModelSerializer, self).to_representation(instance)


class CompanySerializer(ModelSerializer):
    class Meta:
        model = Company
        fields = ('id', 'name', 'adress')


class SizeSerializer(ModelSerializer):
    class Meta:
        model = Size
        fields = ('id', 'label', 'origin')


class CompanyModelSerializer(ModelSerializer):
    # size = SizeSerializer(read_only=True)
    # company = CompanySerializer(read_only=True)
    # clothingtype = ClothingTypeSerializer(read_only=True)

    class Meta:
        model = CompanyModel
        fields = ('id', 'color', 'dimensions',
                  'company', 'size', 'clothingtype')

    def to_representation(self, instance):
        self.fields['company'] = CompanySerializer(read_only=True)
        self.fields['size'] = SizeSerializer(read_only=True)
        self.fields['clothingtype'] = ClothingTypeSerializer(read_only=True)
        return super(CompanyModelSerializer, self).to_representation(instance)
