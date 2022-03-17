from email.policy import default
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from polls.models import ClothingType
from tests.models import ClothingTypeFactory
from rest_framework.test import APIClient

#---------------------------------------------CLOTHINGTYPE VIEW TESTS-----------------------------------------------------#

class ClothingTypeViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.list_url = reverse('clothingtype-list')



    def testGetAll(self):
        """GET to get all ClothingTypes."""
        clothingtype1 = ClothingTypeFactory()
        clothingtype2 = ClothingTypeFactory()
        clothingtype3 = ClothingTypeFactory()
        clothingtype1.save()
        clothingtype2.save()
        clothingtype3.save()
        self.assertEqual(ClothingType.objects.count(), 3)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        all_clothingtypes = ClothingType.objects.all().order_by('id')
        clothingtype1_data = all_clothingtypes[0]
        clothingtype2_data = all_clothingtypes[1]
        clothingtype3_data = all_clothingtypes[2]

        for field_name in ['id', 'label', 'points']: 
            self.assertIsNotNone(getattr(clothingtype1, field_name, None))
            self.assertIsNotNone(getattr(clothingtype1_data, field_name, None))
            self.assertEqual(getattr(clothingtype1, field_name), getattr(clothingtype1_data, field_name))
            self.assertEqual(getattr(clothingtype2, field_name), getattr(clothingtype2_data, field_name))
            self.assertEqual(getattr(clothingtype3, field_name), getattr(clothingtype3_data, field_name))

    def testGetById(self):
        """GET to get ClothingType by Id."""
        clothingtype = ClothingTypeFactory()
        clothingtype.save()
        self.assertEqual(ClothingType.objects.count(), 1)
        response = self.client.get(self.list_url + str(clothingtype.id) + '/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        clothingtype_data = ClothingType.objects.all().first()
        for field_name in ['id', 'label', 'points']: 
            self.assertIsNotNone(getattr(clothingtype, field_name, None))
            self.assertIsNotNone(getattr(clothingtype_data, field_name, None))
            self.assertEqual(getattr(clothingtype, field_name), getattr(clothingtype_data, field_name))
        
    def testPost(self):
        """POST to create a ClothingType."""
        data_clothingtype = {
            'label': 'New label',
            'points': 'New points',
        }
        self.assertEqual(ClothingType.objects.count(), 0)
        response = self.client.post(self.list_url, data=data_clothingtype, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ClothingType.objects.count(), 1)
        clothingtype = ClothingType.objects.all().first()
        for field_name in data_clothingtype.keys():
            self.assertIsNotNone(getattr(clothingtype, field_name, None))
            self.assertIsNotNone(data_clothingtype[field_name])
            self.assertEqual(getattr(clothingtype, field_name), data_clothingtype[field_name])

    def testDelete(self):
        """DELETE to destroy a ClothingType."""
        clothingtype = ClothingTypeFactory()
        clothingtype.save()
        self.assertEqual(ClothingType.objects.count(), 1)
        response = self.client.delete(self.list_url + str(clothingtype.id) + '/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(ClothingType.objects.count(), 0)
