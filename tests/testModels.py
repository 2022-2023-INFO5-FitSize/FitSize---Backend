from django.test import TestCase
from tests.models import ClothingTypeFactory, UserFactory, UserModelFactory, CompanyFactory, CompanyModelFactory, SizeFactory

class FooTest(TestCase):
    def test_str_user(self):
        user = UserFactory(login="Alfred")
        self.assertEqual(str(user), "Alfred")

    def test_str_usermodel(self):
        usermodel = UserModelFactory(name="Alfred")
        self.assertEqual(str(usermodel), "Alfred")

    def test_str_company(self):
        company = CompanyFactory(name="Apple")
        self.assertEqual(str(company), "Apple")

    def test_str_companymodel(self):
        companymodel = CompanyModelFactory(color="Blue")
        self.assertEqual(str(companymodel), "Blue")

    def test_str_user(self):
        size = SizeFactory(label="XS")
        self.assertEqual(str(size), "XS")

    def test_str_clothingtype(self):
        clothingtype = ClothingTypeFactory(label="TShirt")
        self.assertEqual(str(clothingtype), "TShirt")