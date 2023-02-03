from rest_framework.test import APIClient
from django.urls import reverse
from django.test import TestCase
from polls.models import CompanyRepresentative, Company
from tests.models import CompanyRepresentativeFactory, CompanyFactory
from rest_framework import status

#----------------------------------------- COMPANY REPRESENTATIVE VIEW TESTS -------------------------------------------------#

class CompanyViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.list_url = reverse('companyrepresentative-list')



    def testGetAll(self):
        """GET to get all Companys."""
        companyRepresentative1 = CompanyRepresentativeFactory()
        companyRepresentative2 = CompanyRepresentativeFactory()
        companyRepresentative3 = CompanyRepresentativeFactory()
        
        companyRepresentative1.company.save()
        companyRepresentative2.company.save()
        companyRepresentative3.company.save()
        
        companyRepresentative1.save()
        companyRepresentative2.save()
        companyRepresentative3.save()
        
        self.assertEqual(CompanyRepresentative.objects.count(), 3)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        all_companys = CompanyRepresentative.objects.all().order_by('id')
        companyRep1_data = all_companys[0]
        companyRep2_data = all_companys[1]
        companyRep3_data = all_companys[2]
        
        for field_name in ['id', 'login', 'password']: 
            self.assertEqual(getattr(companyRepresentative1, field_name), getattr(companyRep1_data, field_name))
            self.assertEqual(getattr(companyRepresentative2, field_name), getattr(companyRep2_data, field_name))
            self.assertEqual(getattr(companyRepresentative3, field_name), getattr(companyRep3_data, field_name))

    def testGetById(self):
        """GET to get Company by Id."""
        companyRep = CompanyRepresentativeFactory()
        
        companyRep.company.save()
        companyRep.save()
        
        self.assertEqual(CompanyRepresentative.objects.count(), 1)
        response = self.client.get(self.list_url + str(companyRep.id) + '/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        company_data = CompanyRepresentative.objects.all().first()
        for field_name in ['id', 'login', 'password']: 
            self.assertEqual(getattr(companyRep, field_name), getattr(company_data, field_name))
        
    def testPost(self):
        """POST to create a Company."""
        company = CompanyFactory()

        company.save()
        
        data_companyRep = {
            'login': 'croninis',
            'password': 'azerty',
            'company': company.id
        }
        
        self.assertEqual(CompanyRepresentative.objects.count(), 0)
        response = self.client.post(self.list_url, data=data_companyRep, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CompanyRepresentative.objects.count(), 1)
        
        company = CompanyRepresentative.objects.all().first()
        for field_name in ['login', 'password']:
            self.assertEqual(getattr(company, field_name), data_companyRep[field_name])

        #Tests for ForeignKey fields
        self.assertIsInstance(getattr(company, 'company'), Company)
        self.assertEqual(getattr(company, 'company').id, data_companyRep['company'])


    def testDelete(self):
        """DELETE to destroy a Company."""
        companyRep = CompanyRepresentativeFactory()

        companyRep.company.save()
        companyRep.save()

        self.assertEqual(CompanyRepresentative.objects.count(), 1)

        response = self.client.delete(self.list_url + str(companyRep.id) + '/')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(CompanyRepresentative.objects.count(), 0)
