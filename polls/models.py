from django.db import models


class User(models.Model):
    login = models.CharField(max_length=100, blank=True)
    password = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.login


class UserModel(models.Model):
    name = models.CharField(max_length=100, blank=True)
    dimensions = models.CharField(max_length=100, blank=True)
    user = models.ForeignKey(
        'User', on_delete=models.CASCADE, blank=True, null=True)
    clothingtype = models.ForeignKey(
        'ClothingType', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name


class Company(models.Model):
    name = models.CharField(max_length=100, blank=True)
    adress = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.name


class CompanyModel(models.Model):
    color = models.CharField(max_length=100, blank=True)
    dimensions = models.CharField(max_length=1000, blank=True)
    company = models.ForeignKey(
        'Company', on_delete=models.CASCADE, blank=True, null=True)
    size = models.ForeignKey(
        'Size', on_delete=models.CASCADE, blank=True, null=True)
    clothingtype = models.ForeignKey(
        'ClothingType', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.color


class Size(models.Model):
    label = models.CharField(max_length=100, blank=True)
    origin = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.label


class ClothingType(models.Model):
    label = models.CharField(max_length=100, blank=True)
    points = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.label
