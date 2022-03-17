from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from polls.models import Size
from tests.models import SizeFactory
from rest_framework.test import APIClient

#---------------------------------------------SIZE VIEW TESTS-----------------------------------------------------#

class SizeViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.list_url = reverse('size-list')



    def testGetAll(self):
        """GET to get all Sizes."""
        size1 = SizeFactory()
        size2 = SizeFactory()
        size3 = SizeFactory()
        size1.save()
        size2.save()
        size3.save()
        self.assertEqual(Size.objects.count(), 3)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        all_sizes = Size.objects.all().order_by('id')
        size1_data = all_sizes[0]
        size2_data = all_sizes[1]
        size3_data = all_sizes[2]
        for field_name in ['id', 'label', 'origin']: 
            self.assertEqual(getattr(size1, field_name), getattr(size1_data, field_name))
            self.assertEqual(getattr(size2, field_name), getattr(size2_data, field_name))
            self.assertEqual(getattr(size3, field_name), getattr(size3_data, field_name))

    def testGetById(self):
        """GET to get Size by Id."""
        size = SizeFactory()
        size.save()
        self.assertEqual(Size.objects.count(), 1)
        response = self.client.get(self.list_url + str(size.id) + '/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        size_data = Size.objects.all().first()
        for field_name in ['id', 'label', 'origin']: 
            self.assertEqual(getattr(size, field_name), getattr(size_data, field_name))
        
    def testPost(self):
        """POST to create a Size."""
        data_size = {
            'label': 'New label',
            'origin': 'New origin',
        }
        self.assertEqual(Size.objects.count(), 0)
        response = self.client.post(self.list_url, data=data_size, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Size.objects.count(), 1)
        size = Size.objects.all().first()
        for field_name in data_size.keys():
            self.assertEqual(getattr(size, field_name), data_size[field_name])

    def testDelete(self):
        """DELETE to destroy a Size."""
        size = SizeFactory()
        size.save()
        self.assertEqual(Size.objects.count(), 1)
        response = self.client.delete(self.list_url + str(size.id) + '/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Size.objects.count(), 0)
