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
        usermodel = models.UserModelFactory()
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
