from django.test import TestCase
from rest_framework.test import APITestCase

# Create your tests here.



class test_courses(APITestCase):
    
    def setUp(self):
        self.var = 12

    def test_create_course(self):
        self.var=15;
        self.assertEqual(self.var,15)


