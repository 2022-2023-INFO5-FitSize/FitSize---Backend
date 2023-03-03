from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from polls.models import CompanyModel, Company, Image, Size, ClothingType
from tests.models import CompanyModelFactory, CompanyFactory, ImageFactory, SizeFactory, ClothingTypeFactory
from rest_framework.test import APIClient

#---------------------------------------------COMPANYMODEL VIEW TESTS-----------------------------------------------------#


class CompanyModelViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.list_url = reverse('companymodel-list')


    def assertField(self, field_name, data_source_object, data_result_object):
        self.assertEqual(getattr(data_source_object, field_name), getattr(data_result_object, field_name))

    def assertFields(self, fields, data_source_object, data_result_object):
        for field in fields:
            self.assertField(field, data_source_object, data_result_object)

    def testGetAll(self):
        """GET to get all CompanyModels."""
        companymodel1 = CompanyModelFactory()
        companymodel2 = CompanyModelFactory()

        companymodel1.company.save()
        companymodel1.size.save()
        companymodel1.clothingtype.save()
        
         # save all images associated with companymodel1
        for image in companymodel1.images.all():
            image.save()

        companymodel2.company.save()
        companymodel2.size.save()
        companymodel2.clothingtype.save()

        # save all images associated with companymodel2
        for image in companymodel2.images.all():
            image.save()

        companymodel1.save()
        companymodel2.save()


        # assert the number of CompanyModel is the same 
        # as those we defined earlier
        self.assertEqual(CompanyModel.objects.count(), 2)

        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        all_companymodels = CompanyModel.objects.all().order_by('id')
        companymodel1_data = all_companymodels[0]
        companymodel2_data = all_companymodels[1]

        self.assertFields(['id', 'color', 'dimensions'], companymodel1, companymodel1_data)
        self.assertFields(['id', 'color', 'dimensions'], companymodel2, companymodel2_data)

        for i in range(0, companymodel1.images.count() - 1):
            self.assertFields(['id','image'], companymodel1.images.all()[i], companymodel1_data.images.all()[i])

        for i in range(0, companymodel2.images.count() - 1):
            self.assertFields(['id','image'], companymodel2.images.all()[i], companymodel2_data.images.all()[i])
            

    def testGetById(self):
        """GET to get CompanyModel by Id."""
        companymodel = CompanyModelFactory()
       
        companymodel.company.save()
        companymodel.size.save()
        companymodel.clothingtype.save()
       
        # save all images associated with companymodel2
        for image in companymodel.images.all():
            image.save()
       
        companymodel.save()
        
        self.assertEqual(CompanyModel.objects.count(), 1)
        
        response = self.client.get(self.list_url + str(companymodel.id) + '/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        companymodel_data = CompanyModel.objects.all().first()
        
        self.assertFields(['id', 'color', 'dimensions'], companymodel, companymodel_data)

        # Assert all the images exist and are identical
        for i in range(0, companymodel.images.count() - 1):
            self.assertFields(['id','image'], companymodel.images.all()[i], companymodel_data.images.all()[i])


    def testPost(self):
        """POST to create a CompanyModel."""
        company = CompanyFactory()
        size = SizeFactory()
        clothingtype = ClothingTypeFactory()

        company.save()
        size.save()
        clothingtype.save()

        # Create two Image instances for the UserModel
        image1 = ImageFactory()
        image2 = ImageFactory()

        image1.save()
        image2.save()

        data_companymodel = {
            'color': 'New color',
            'dimensions': 'New dimensions',
            'company': company.id,
            'size': size.id,
            'clothingtype': clothingtype.id,
        }
        
        data_companymodel['images'] = [image1.id, image2.id]

        
        # at the begining, there is no objects in UserModel
        self.assertEqual(CompanyModel.objects.count(), 0)
        # we will post the data
        response = self.client.post(self.list_url, data=data_companymodel, format='json')
        # ensure that the response is good
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # new object created
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

        # Assert all the images exist and are identical
        for i in range(0, companymodel.images.count()):
            image = companymodel.images.all()[i]

            self.assertIsInstance(image, Image)
            self.assertEqual(image.id, data_companymodel['images'][i])


    def testDelete(self):
        """DELETE to destroy a CompanyModel."""
        companymodel = CompanyModelFactory()
        
        companymodel.company.save()
        companymodel.size.save()
        companymodel.clothingtype.save()
        
        # save all images associated with companymodel2
        for image in companymodel.images.all():
            image.save()
        
        companymodel.save()
        
        self.assertEqual(CompanyModel.objects.count(), 1)
        response = self.client.delete(
            self.list_url + str(companymodel.id) + '/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(CompanyModel.objects.count(), 0)
