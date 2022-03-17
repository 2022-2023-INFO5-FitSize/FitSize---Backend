from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from polls.models import Company
from tests.models import CompanyFactory
from rest_framework.test import APIClient

#---------------------------------------------COMPANY VIEW TESTS-----------------------------------------------------#

class CompanyViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.list_url = reverse('company-list')



    def testGetAll(self):
        """GET to get all Companys."""
        company1 = CompanyFactory()
        company2 = CompanyFactory()
        company3 = CompanyFactory()
        company1.save()
        company2.save()
        company3.save()
        self.assertEqual(Company.objects.count(), 3)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        all_companys = Company.objects.all().order_by('id')
        company1_data = all_companys[0]
        company2_data = all_companys[1]
        company3_data = all_companys[2]
        for field_name in ['id', 'name', 'adress']: 
            self.assertEqual(getattr(company1, field_name), getattr(company1_data, field_name))
            self.assertEqual(getattr(company2, field_name), getattr(company2_data, field_name))
            self.assertEqual(getattr(company3, field_name), getattr(company3_data, field_name))

    def testGetById(self):
        """GET to get Company by Id."""
        company = CompanyFactory()
        company.save()
        self.assertEqual(Company.objects.count(), 1)
        response = self.client.get(self.list_url + str(company.id) + '/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        company_data = Company.objects.all().first()
        for field_name in ['id', 'name', 'adress']: 
            self.assertEqual(getattr(company, field_name), getattr(company_data, field_name))
        
    def testPost(self):
        """POST to create a Company."""
        data_company = {
            'name': 'New name',
            'adress': 'New adress',
        }
        self.assertEqual(Company.objects.count(), 0)
        response = self.client.post(self.list_url, data=data_company, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Company.objects.count(), 1)
        company = Company.objects.all().first()
        for field_name in data_company.keys():
            self.assertEqual(getattr(company, field_name), data_company[field_name])

    def testDelete(self):
        """DELETE to destroy a Company."""
        company = CompanyFactory()
        company.save()
        self.assertEqual(Company.objects.count(), 1)
        response = self.client.delete(self.list_url + str(company.id) + '/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Company.objects.count(), 0)
