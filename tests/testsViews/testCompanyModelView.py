from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from polls.models import CompanyModel, Company, Size, ClothingType
from tests.models import CompanyModelFactory, CompanyFactory, SizeFactory, ClothingTypeFactory
from rest_framework.test import APIClient

#---------------------------------------------COMPANYMODEL VIEW TESTS-----------------------------------------------------#


class CompanyModelViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.list_url = reverse('companymodel-list')

    def testGetAll(self):
        """GET to get all CompanyModels."""
        companymodel1 = CompanyModelFactory()
        companymodel2 = CompanyModelFactory()
        companymodel3 = CompanyModelFactory()

        companymodel1.company.save()
        companymodel1.size.save()
        companymodel1.clothingtype.save()

        companymodel2.company.save()
        companymodel2.size.save()
        companymodel2.clothingtype.save()

        companymodel3.company.save()
        companymodel3.size.save()
        companymodel3.clothingtype.save()

        companymodel1.save()
        companymodel2.save()
        companymodel3.save()

        self.assertEqual(CompanyModel.objects.count(), 3)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        all_companymodels = CompanyModel.objects.all().order_by('id')
        companymodel1_data = all_companymodels[0]
        companymodel2_data = all_companymodels[1]
        companymodel3_data = all_companymodels[2]
        for field_name in ['id', 'color', 'dimensions']:
            self.assertEqual(getattr(companymodel1, field_name),
                             getattr(companymodel1_data, field_name))
            self.assertEqual(getattr(companymodel2, field_name),
                             getattr(companymodel2_data, field_name))
            self.assertEqual(getattr(companymodel3, field_name),
                             getattr(companymodel3_data, field_name))

    def testGetById(self):
        """GET to get CompanyModel by Id."""
        companymodel = CompanyModelFactory()
        companymodel.company.save()
        companymodel.size.save()
        companymodel.clothingtype.save()
        companymodel.save()
        self.assertEqual(CompanyModel.objects.count(), 1)
        response = self.client.get(self.list_url + str(companymodel.id) + '/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        companymodel_data = CompanyModel.objects.all().first()
        for field_name in ['id', 'color', 'dimensions']:
            self.assertEqual(getattr(companymodel, field_name),
                             getattr(companymodel_data, field_name))

    def testPost(self):
        """POST to create a CompanyModel."""
        company = CompanyFactory()
        size = SizeFactory()
        clothingtype = ClothingTypeFactory()

        company.save()
        size.save()
        clothingtype.save()

        data_companymodel = {
            'color': 'New color',
            'dimensions': 'New dimensions',
            'company': company.id,
            'size': size.id,
            'clothingtype': clothingtype.id,
        }
        self.assertEqual(CompanyModel.objects.count(), 0)
        response = self.client.post(self.list_url, data=data_companymodel, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CompanyModel.objects.count(), 1)
        companymodel = CompanyModel.objects.all().first()
        for field_name in ['color', 'dimensions']:
            self.assertEqual(getattr(companymodel, field_name),
                             data_companymodel[field_name])
        #Tests for ForeignKey fields
        self.assertIsInstance(getattr(companymodel, 'company'), Company)
        self.assertEqual(getattr(companymodel, 'company').id, data_companymodel['company'])
        self.assertIsInstance(getattr(companymodel, 'size'), Size)
        self.assertEqual(getattr(companymodel, 'size').id, data_companymodel['size'])
        self.assertIsInstance(getattr(companymodel, 'clothingtype'), ClothingType)
        self.assertEqual(getattr(companymodel, 'clothingtype').id, data_companymodel['clothingtype'])

    def testDelete(self):
        """DELETE to destroy a CompanyModel."""
        companymodel = CompanyModelFactory()
        companymodel.company.save()
        companymodel.size.save()
        companymodel.clothingtype.save()
        companymodel.save()
        self.assertEqual(CompanyModel.objects.count(), 1)
        response = self.client.delete(
            self.list_url + str(companymodel.id) + '/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(CompanyModel.objects.count(), 0)
