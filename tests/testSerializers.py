# import uuid
from django.test import TestCase
from polls import serializers

from tests import models

class UserSerializer(TestCase):
    def test_model_fields(self):
        user = models.UserFactory()
        serializer = serializers.UserSerializer(user)
        for field_name in [
            'id','login', 'password'
        ]:
            self.assertEqual(
                serializer.data[field_name],
                getattr(user, field_name)
            )

# class UserModel(TestCase):
#     def test_model_fields(self):
#         usermodel = models.UserModelFactory()
#         serializer = serializers.UserModelSerializer(usermodel)
#         for field_name in [
#             'id', 'name', 'dimensions', 'user', 'clothingtype'
#         ]:
#             self.assertEqual(
#                 serializer.data[field_name],
#                 getattr(usermodel, field_name)
#             )

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

# class CompanyModelSerializer(TestCase):
#     def test_model_fields(self):
#         companymodel = models.CompanyModelFactory()
#         serializer = serializers.CompanyModelSerializer(companymodel)
#         for field_name in ['id', 'color', 'dimensions']:
#             self.assertEqual(
#                 serializer.data[field_name],
#                 getattr(companymodel, field_name)
#             )
#         for field_name in ['company', 'size', 'clothingtype']:
#             self.assertEqual(
#                 serializer.data[field_name],
#                 getattr(companymodel, field_name)
#             )

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