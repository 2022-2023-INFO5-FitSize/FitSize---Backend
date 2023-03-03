import factory
import factory.fuzzy
from faker import Faker
import uuid
from polls.models import Image, ClothingType, Company, Model, User, UserModel, CompanyModel, Size, CompanyRepresentative
from django.db import models
import random
import secrets

class ImageFactory(factory.Factory):
    class Meta:
        model = Image

    # generate random image
    # using this way to have a different image
    # each time ImageFactory is called
    image = factory.LazyAttribute(lambda obj: secrets.token_bytes(64))

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
    class Meta:
        model = UserModel

    id = factory.Sequence(lambda n: n)
    name = factory.Faker('name')
    user = factory.SubFactory(UserFactory)


    dimensions = "{'neckline': 5.2, 'center_front': 10.3, 'shoulder': 5.8, 'armpit': 10.3, 'cuff_left': 9.4}"
    clothingtype = factory.SubFactory(ClothingTypeFactory)
    
    # Define the RelatedFactory for Image objects
    #images = factory.SubFactory(ImageFactory, size=3)
    #images = factory.SubFactory(ImageFactory, 'image')
    
    @factory.post_generation
    def images_gen(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        # we will generate 2 images for each UserModel
        for i in range(0, 3):
            image = ImageFactory()
            image.save()
            self.images.add(image)

class CompanyFactory(factory.Factory):
    name = factory.Faker('company')
    adress = factory.Faker('address')

    class Meta:
        model = Company


class CompanyRepresentativeFactory(factory.Factory):
    login = factory.Faker('name')
    password = factory.Faker('password')
    company = factory.SubFactory(CompanyFactory)

    
    class Meta:
        model = CompanyRepresentative

class SizeFactory(factory.Factory):
    label = "XS"
    origin = factory.Faker('country')

    class Meta:
        model = Size


class CompanyModelFactory(factory.Factory):
    id = factory.Sequence(lambda n: n)
    color = factory.Faker('color')
    company = factory.SubFactory(CompanyFactory)
    size = factory.SubFactory(SizeFactory)
    
    dimensions = "{'neckline': 5.2, 'center_front': 10.3, 'shoulder': 5.8, 'armpit': 10.3, 'cuff_left': 9.4}"
    clothingtype = factory.SubFactory(ClothingTypeFactory)

    # Define the RelatedFactory for Image objects
    images = factory.RelatedFactoryList(ImageFactory, size=lambda: random.randint(1, 5))

    
    class Meta:
        model = CompanyModel
