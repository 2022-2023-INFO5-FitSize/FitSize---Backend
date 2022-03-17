import factory
import uuid
from polls.models import ClothingType, Company, User, UserModel, CompanyModel, Size
from django.db import models


class UserFactory(factory.Factory):
    login = factory.Faker('name')
    password = factory.Faker('password')

    class Meta:
        model = User


class ClothingTypeFactory(factory.Factory):
    label = "XS"
    points = "200 10 100"

    class Meta:
        model = ClothingType


class UserModelFactory(factory.Factory):
    name = factory.Faker('name')
    dimensions = "1.0,0.1,4.0,2.5,4.0KP0.0,0.5,8.0,7.0,6.0,5.5,1.2,7.8,8.8,0.0,9.4,8.0"
    user = factory.SubFactory(UserFactory)
    clothingtype = factory.SubFactory(ClothingTypeFactory)

    class Meta:
        model = UserModel


class CompanyFactory(factory.Factory):
    name = factory.Faker('company')
    adress = factory.Faker('address')

    class Meta:
        model = Company


class SizeFactory(factory.Factory):
    label = "XS"
    origin = factory.Faker('country')

    class Meta:
        model = Size


class CompanyModelFactory(factory.Factory):
    color = factory.Faker('color')
    dimensions = "200 10 100"
    company = factory.SubFactory(CompanyFactory)
    size = factory.SubFactory(SizeFactory)
    clothingtype = factory.SubFactory(ClothingTypeFactory)

    class Meta:
        model = CompanyModel
