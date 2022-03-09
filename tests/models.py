import factory
import uuid
from django.test import TestCase
from polls.models import User, UserModel
from django.db import models

class UserFactory(factory.Factory):
    id = models.UUIDField(
         primary_key = True,
         default = uuid.uuid4,
         editable = False)
    login = factory.Faker('login')
    password = factory.Faker('password')
    class Meta:
        model = User

# class UserTest(TestCase):
#     id = 1
#     login = "Adam"
#     password = "password"
#     def __str__(self):
#         return self.login

class UserModelFactory(UserModel):
    id = models.UUIDField(primary_key = True,
         default = uuid.uuid4,
         editable = False)
    name = factory.Faker('name')
    dimensions = "200 10 100" #Syntaxe des dimensions à définir
    # user = User(id = 1, login = "John", password = "One")
    # clothingtype = ClothingType(id = 1, label = "Robe", points = "1 0 0 0.1")
    class Meta:
        model = UserModel
    
    @factory.post_generation
    def user(obj, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            assert isinstance(extracted, int)
            UserFactory.create_batch(size=extracted, **kwargs)

# class UserModelTest(TestCase):
#     id = 1
#     name = "TShirt"
#     dimensions = "200 10 100" #Syntaxe des dimensions à définir
#     user = User(id = 1, login = "John", password = "One")
#     clothingtype = ClothingType(id = 1, label = "Robe", points = "1 0 0 0.1")
#     def __str__(self):
#         return self.name + " " + self.user.login

# class Company(TestCase):
#     id = models.IntegerField(primary_key=True)
#     name = models.CharField(max_length=100, blank=True)
#     adress = models.CharField(max_length=200, blank=True)
#     def __str__(self):
#         return self.name

# class CompanyModel(TestCase):
#     id = models.IntegerField(primary_key=True)
#     color = models.CharField(max_length=100, blank=True)
#     dimensions = models.CharField(max_length=100, blank=True)
#     company = models.ForeignKey( 'Company', on_delete=models.CASCADE, blank=True, null=True)
#     size = models.ForeignKey( 'Size', on_delete=models.CASCADE, blank=True, null=True)
#     clothingtype = models.ForeignKey( 'ClothingType', on_delete=models.CASCADE, blank=True, null=True)
#     def __str__(self):
#         return self.id

# class Size(TestCase):
#     id = models.IntegerField(primary_key=True)
#     label = models.CharField(max_length=100, blank=True)
#     origin = models.CharField(max_length=100, blank=True)
#     def __str__(self):
#         return self.label

# class ClothingType(TestCase):
#     id = models.IntegerField(primary_key=True)
#     label = models.CharField(max_length=100, blank=True)
#     points = models.CharField(max_length=200, blank=True)
#     def __str__(self):
#         return self.label