import uuid
from django.db import models



class User(models.Model):
    login = models.CharField(max_length=100, blank=True)
    password = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return "USER : login : " + self.login + " password : " + self.password


class UserModel(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    name = models.CharField(max_length=100, blank=True)
    dimensions = models.CharField(max_length=100, blank=True)
    user = models.ForeignKey(
        'User', on_delete=models.CASCADE, blank=True, null=True)
    clothingtype = models.ForeignKey(
        'ClothingType', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return "USERMODEL : name : " + self.name + " dimensions : " + self.dimensions + " user with login : " + self.user.login + " clothing type with label : " + self.clothingtype.label 

class Company(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    name = models.CharField(max_length=100, blank=True)
    adress = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.name


class CompanyModel(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    color = models.CharField(max_length=100, blank=True)
    dimensions = models.CharField(max_length=1000, blank=True)
    company = models.ForeignKey(
        'Company', on_delete=models.CASCADE, blank=True, null=True)
    size = models.ForeignKey(
        'Size', on_delete=models.CASCADE, blank=True, null=True)
    clothingtype = models.ForeignKey(
        'ClothingType', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.id


class Size(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    label = models.CharField(max_length=100, blank=True)
    origin = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.label


class ClothingType(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    label = models.CharField(max_length=100, blank=True)
    points = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.label
