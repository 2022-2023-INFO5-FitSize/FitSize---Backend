from rest_framework.serializers import ModelSerializer

from polls.models import ClothingType, Image, Company, CompanyModel, Model, Size, User, UserModel, CompanyRepresentative

class ImageSerializer(ModelSerializer):
    class Meta:
        model = Image
        fields = ('id', 'image')

class ModelSerial(ModelSerializer):
    images = ImageSerializer(many=True)

    class Meta:
        model = Model        
        fields = ('id', 'dimensions', 'clotingtype', 'images')
        
    def to_representation(self, instance):
        self.fields['clothingtype'] = ClothingTypeSerializer(read_only=True)
    
        return super(ModelSerial, self).to_representation(instance)

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'login', 'password')


class ClothingTypeSerializer(ModelSerializer):
    class Meta:
        model = ClothingType
        fields = ('id', 'label', 'points')


class UserModelSerializer(ModelSerializer):
    images = ImageSerializer(many=True)
    
    class Meta:
        model = UserModel
        fields = '__all__'
        
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
    company = CompanySerializer(read_only=True)
    images = ImageSerializer(read_only=True, many=True)

    class Meta:
        model = CompanyModel
        fields = ('id', 'color', 'dimensions',
                  'company', 'size', 'clothingtype')

    def to_representation(self, instance):
        self.fields['company'] = CompanySerializer(read_only=True)
        self.fields['size'] = SizeSerializer(read_only=True)
        self.fields['clothingtype'] = ClothingTypeSerializer(read_only=True)
        return super(CompanyModelSerializer, self).to_representation(instance)
    
class CompanyRepresentativeSerializer(ModelSerializer):
    class Meta:
        model = CompanyRepresentative
        fields = ('id', 'login', 'password', 'company')
        
    def to_representation(self, instance):
        self.fields['company'] = CompanySerializer(read_only=True)
        return super(CompanyRepresentativeSerializer, self).to_representation(instance)

