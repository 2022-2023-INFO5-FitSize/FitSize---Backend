from django.test import TestCase
from polls import serializers
from tests import models


class UserSerializer(TestCase):
    def test_model_fields(self):
        user = models.UserFactory()
        serializer = serializers.UserSerializer(user)
        for field_name in [
            'id', 'login', 'password'
        ]:
            self.assertEqual(
                serializer.data[field_name],
                getattr(user, field_name)
            )


class UserModelSerializer(TestCase):
    def test_model_fields(self):
        
        """
        user = models.UserFactory.create()
        clothing_type = models.ClothingTypeFactory.create()
        images = models.ImageFactory.create()

        user.save()
        clothing_type.save()
        images.save()
        """
        usermodel = models.UserModelFactory.create()
        usermodel.clothingtype.save()
        usermodel.user.save()
        
        image1 = models.ImageFactory.create()
        image2 = models.ImageFactory.create()
        image1.save()
        image2.save()
        
        usermodel.save()
        usermodel.images.add(image1, image2)
        usermodel.save()

        serializer = serializers.UserModelSerializer(usermodel)
        
        for field_name in ['id', 'name', 'dimensions']:
            self.assertEqual(
                serializer.data[field_name],
                getattr(usermodel, field_name)
            )
        
        # Equivalence with user field
        for field_name in ['id', 'login', 'password']:
            self.assertEqual(
                serializer.data['user'][field_name],
                getattr(usermodel.user, field_name)
            )
        # Equivalence between clothingtype field
        for field_name in ['id', 'label', 'points']:
            self.assertEqual(
                serializer.data['clothingtype'][field_name],
                getattr(usermodel.clothingtype, field_name)
            )
            
        print("1", str(usermodel.images.values()[0]['image']))
        print("2", serializer.data["images"][0]['image'])

        for i, image in enumerate(serializer.data['images']):
            for field_name in ['id', 'image']:     
                self.assertEqual(
                    image[field_name],
                    getattr(usermodel.images.all()[i], field_name)
                )

class CompanySerializer(TestCase):
    def test_model_fields(self):
        company = models.CompanyFactory()
        serializer = serializers.CompanySerializer(company)
        for field_name in [
            'id', 'name', 'adress'
        ]:
            self.assertEqual(
                serializer.data[field_name],
                getattr(company, field_name)
            )


class CompanyRepresentativeSerializer(TestCase):
    def test_model_fields(self):
        companyRepresentative = models.CompanyRepresentativeFactory()
        serializer = serializers.CompanyRepresentativeSerializer(companyRepresentative)

        for field_name in [
            'id', 'login', 'password'
        ]:
            self.assertEqual(
                serializer.data[field_name],
                getattr(companyRepresentative, field_name)
            )
        
        # Equivalence between company field
        for field_name in ['id', 'name', 'adress']:
            self.assertEqual(
                serializer.data['company'][field_name],
                getattr(companyRepresentative.company, field_name)
            )

class CompanyModelSerializer(TestCase):
    def test_model_fields(self):
        companymodel = models.CompanyModelFactory()
        serializer = serializers.CompanyModelSerializer(companymodel)
        for field_name in ['id', 'color', 'dimensions']:
            self.assertEqual(
                serializer.data[field_name],
                getattr(companymodel, field_name)
            )
        # Equivalence between company field
        for field_name in ['id', 'name', 'adress']:
            self.assertEqual(
                serializer.data['company'][field_name],
                getattr(companymodel.company, field_name)
            )
        # Equivalence between size field
        for field_name in ['id', 'label', 'origin']:
            self.assertEqual(
                serializer.data['size'][field_name],
                getattr(companymodel.size, field_name)
            )
        # Equivalence between clothingtype field
        for field_name in ['id', 'label', 'points']:
            self.assertEqual(
                serializer.data['clothingtype'][field_name],
                getattr(companymodel.clothingtype, field_name)
            )

        for i, image in enumerate(serializer.data['images']):
            for field_name in ['id', 'image']:
                """print("=======================================")
                print(str(i) + "\t" + field_name)
                print("=======================================")

                print(serializer.data['images'][i][field_name])
                print("---------------------------------------")
                print(usermodel.images.values()[i][field_name])
                """
                self.assertEqual(
                    image[field_name].encode('utf-8'),
                    getattr(companymodel.images.all()[i].encode('utf-8'), field_name)
                )



class SizeSerializer(TestCase):
    def test_model_fields(self):
        size = models.SizeFactory()
        serializer = serializers.SizeSerializer(size)
        for field_name in [
            'id', 'label', 'origin'
        ]:
            self.assertEqual(
                serializer.data[field_name],
                getattr(size, field_name)
            )


class ClothingTypeSerializer(TestCase):
    def test_model_fields(self):
        clothingtype = models.ClothingTypeFactory()
        serializer = serializers.ClothingTypeSerializer(clothingtype)
        for field_name in [
            'id', 'label', 'points'
        ]:
            self.assertEqual(
                serializer.data[field_name],
                getattr(clothingtype, field_name)
            )
