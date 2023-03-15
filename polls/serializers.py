from rest_framework.serializers import ModelSerializer

from polls.models import ClothingType, Company, CompanyModel, Model, Size, User, UserModel, CompanyRepresentative

class ModelSerial(ModelSerializer):
    class Meta:
        model = Model        
        fields = ('id', 'dimensions', 'clotingtype', 'image')
        
    def to_representation(self, instance):
        self.fields['clothingtype'] = ClothingTypeSerializer(read_only=True)
        return super(ModelSerial, self).to_representation(instance)

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'login', 'password')

    def to_representation(self, instance):
        return super(UserSerializer, self).to_representation(instance)


class ClothingTypeSerializer(ModelSerializer):
    class Meta:
        model = ClothingType
        fields = ('id', 'label', 'points')


class UserModelSerializer(ModelSerializer):
    
    class Meta:
        model = UserModel
        fields = ('id', 'name', 'user', 'dimensions', 'clothingtype', 'image')
        
    def to_representation(self, instance):
        self.fields['user'] = UserSerializer(read_only=True)
        self.fields['clothingtype'] = ClothingTypeSerializer(read_only=True)

        with instance.image.open() as f:
            content = f.read()

        base64_content = base64.b64encode(content).decode('utf-8')
        # Convert image to base64
        instance.image = base64_content

        return super(UserModelSerializer, self).to_representation(instance)


class CompanySerializer(ModelSerializer):
    class Meta:
        model = Company
        fields = ('id', 'name', 'adress')


class SizeSerializer(ModelSerializer):
    class Meta:
        model = Size
        fields = ('id', 'label', 'origin')
        
import base64

class CompanyModelSerializer(ModelSerializer):

    class Meta:
        model = CompanyModel
        fields = ('id', 'color', 'dimensions', 'company', 'size', 'clothingtype', 'image')

    def to_representation(self, instance):
        print("to representation companyModel")
        print(instance)

        self.fields['company'] = CompanySerializer(read_only=True)
        self.fields['size'] = SizeSerializer(read_only=True)
        self.fields['clothingtype'] = ClothingTypeSerializer(read_only=True)

        with instance.image.open() as f:
            content = f.read()

        base64_content = base64.b64encode(content).decode('utf-8')
        # Convert image to base64
        instance.image = base64_content

        return super(CompanyModelSerializer, self).to_representation(instance)
    
class CompanyRepresentativeSerializer(ModelSerializer):
    class Meta:
        model = CompanyRepresentative
        fields = ('id', 'login', 'password', 'company')
        
    def to_representation(self, instance):
        self.fields['company'] = CompanySerializer(read_only=True)
        return super(CompanyRepresentativeSerializer, self).to_representation(instance)

