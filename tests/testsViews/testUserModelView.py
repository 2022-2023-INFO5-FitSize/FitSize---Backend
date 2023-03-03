from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from polls.models import Image, UserModel, User, ClothingType
from tests.models import ImageFactory, UserModelFactory, UserFactory, ClothingTypeFactory
from rest_framework.test import APIClient

#---------------------------------------------USERMODEL VIEW TESTS-----------------------------------------------------#


class UserModelViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.list_url = reverse('usermodel-list')

    def assertField(self, field_name, data_source_object, data_result_object):
        self.assertEqual(getattr(data_source_object, field_name), getattr(data_result_object, field_name))

    def assertFields(self, fields, data_source_object, data_result_object):
        for field in fields:
            self.assertField(field, data_source_object, data_result_object)

    def testGetAll(self):
        """GET to get all UserModels."""
        usermodel1 = UserModelFactory()
        usermodel2 = UserModelFactory()

        usermodel1.user.save()
        usermodel1.clothingtype.save()
        
        # save all images associated with usermodel1
        for image in usermodel1.images.all():
            image.save()
        
        usermodel2.user.save()
        usermodel2.clothingtype.save()

        # save all images associated with usermodel2
        for image in usermodel2.images.all():
            image.save()

        usermodel1.save()
        usermodel2.save()

        # assert the number of UserModel is the same 
        # as those we defined earlier
        self.assertEqual(UserModel.objects.count(), 2)

        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # get all userModel
        all_usermodels = UserModel.objects.all().order_by('id')
        usermodel1_data = all_usermodels[0]
        usermodel2_data = all_usermodels[1]
        
        self.assertFields(['id', 'name', 'dimensions'], usermodel1, usermodel1_data)
        self.assertFields(['id', 'name', 'dimensions'], usermodel2, usermodel2_data)
        
        for i in range(0, usermodel1.images.count() - 1):
            self.assertFields(['id','image'], usermodel1.images.all()[i], usermodel1_data.images.all()[i])

        for i in range(0, usermodel2.images.count() - 1):
            self.assertFields(['id','image'], usermodel2.images.all()[i], usermodel2_data.images.all()[i])
        
        
        
            
    def testGetById(self):
        """GET to get UserModel by Id."""
        usermodel = UserModelFactory()
        
        usermodel.user.save()
        usermodel.clothingtype.save()
        
        # save all images associated with usermodel2
        for image in usermodel.images.all():
            image.save()
        
        usermodel.save()
        
        self.assertEqual(UserModel.objects.count(), 1)
        
        response = self.client.get(self.list_url + str(usermodel.id) + '/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        usermodel_data = UserModel.objects.all().first()
        
        self.assertFields(['id', 'name', 'dimensions'], usermodel, usermodel_data)
        
        # Assert all the images exist and are identical
        for i in range(0, usermodel.images.count() - 1):
            self.assertFields(['id','image'], usermodel.images.all()[i], usermodel_data.images.all()[i])
        

    def testPost(self):
        """POST to create a UserModel."""
        user = UserFactory()
        clothingtype = ClothingTypeFactory()

        user.save()
        clothingtype.save()

        # Create two Image instances for the UserModel
        image1 = ImageFactory()
        image2 = ImageFactory()

        image1.save()
        image2.save()
        
        data_usermodel = {
            'name': 'New name',
            'dimensions': 'New dimensions',
            'user': user.id,
            'clothingtype': clothingtype.id,
        }
        
        data_usermodel['images'] = [image1.id, image2.id]
        
        # at the begining, there is no objects in UserModel
        self.assertEqual(UserModel.objects.count(), 0)
        # we will post the data
        response = self.client.post(self.list_url, data=data_usermodel, format='json')
        # ensure that the response is good
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # new object created
        self.assertEqual(UserModel.objects.count(), 1)

        usermodel = UserModel.objects.all().first()
        for field_name in ['name', 'dimensions']:
            self.assertEqual(getattr(usermodel, field_name),
                             data_usermodel[field_name])
        
        # Tests for ForeignKey fields
        self.assertIsInstance(getattr(usermodel, 'user'), User)
        self.assertEqual(getattr(usermodel, 'user').id, data_usermodel['user'])
        self.assertIsInstance(getattr(usermodel, 'clothingtype'), ClothingType)
        self.assertEqual(getattr(usermodel, 'clothingtype').id,
                         data_usermodel['clothingtype'])

        # Assert all the images exist and are identical
        for i in range(0, usermodel.images.count()):
            image = usermodel.images.all()[i]

            self.assertIsInstance(image, Image)
            self.assertEqual(image.id, data_usermodel['images'][i])


    def testCreateDimensions(self):
        """POST to create a UserModel."""
        user = UserFactory()
        clothingtype = ClothingTypeFactory()

        user.save()
        clothingtype.save()

        data_usermodel = {
            'name': 'New name',
            'dimensions': '1.0,0.1,4.0,2.5,4.0KP0.0,0.5,8.0,7.0,6.0,5.5,1.2,7.8,8.8,0.0,9.4,8.0',
            'user': user.id,
            'clothingtype': clothingtype.id,
        }

        self.assertEqual(UserModel.objects.count(), 0)
        response = self.client.post(
            self.list_url + 'savedimensions/', data_usermodel, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(UserModel.objects.count(), 1)
        usermodel = UserModel.objects.all().first()
        self.assertEqual(getattr(usermodel, 'name'),
                         data_usermodel['name'])
        # Tests for ForeignKey fields
        self.assertIsInstance(getattr(usermodel, 'user'), User)
        self.assertEqual(getattr(usermodel, 'user').id, data_usermodel['user'])
        self.assertIsInstance(getattr(usermodel, 'clothingtype'), ClothingType)
        self.assertEqual(getattr(usermodel, 'clothingtype').id,
                         data_usermodel['clothingtype'])
        self.assertEqual(len(getattr(usermodel, 'dimensions').split(',')), 3)

    def testDelete(self):
        """DELETE to destroy a UserModel."""
        usermodel = UserModelFactory()
        
        usermodel.user.save()
        usermodel.clothingtype.save()
        
        # save all images associated with usermodel
        for image in usermodel.images.all():
            image.save()
        
        usermodel.save()
        # new object created
        self.assertEqual(UserModel.objects.count(), 1)
        # delete the created instance
        response = self.client.delete(self.list_url + str(usermodel.id) + '/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(UserModel.objects.count(), 0)
