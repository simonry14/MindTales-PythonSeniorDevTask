from rest_framework import status
from rest_framework.test import APITestCase

from django.urls import reverse

from api.models import Employee, Restaurant, Menu, Vote, User

class TestRegisterUser(APITestCase):
    def test_register_user(self):
        data = {
            "email":"test@test.com",
            "username":"user1",
            "password":"pass123"
        }
        result = self.client.post(reverse("api:register"), data=data)
        status = result.json().get('success')
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(status, True)
        
class TestLoginUser(APITestCase):
    def test_login_user(self):
        data = {
            "username":"user1",
            "password":"pass123",
            "email":"test@test.com",
        }
        result = self.client.post(reverse("api:login"), data=data)
        status = result.json().get('success')
        self.assertEqual(status, True)
        
        
class TestCreateRestaurant(APITestCase):
    def test_create_restaurant(self):
        data = {
            "name":"Test Restaurant",
            "address":"123 Test Street",
            "created_by":"user1"
        }
        result = self.client.post(reverse("api:create_restaurant"), data=data)
        status = result.json().get('success')
        self.assertEqual(Restaurant.objects.count(), 1)
        self.assertEqual(status, True)
        
class TestCreateMenu(APITestCase):
    def test_create_menu(self):
        data = {
            "restaurant":"1",
            "file":"test.jpg",
            "uploaded_by":"user1"
        }
        result = self.client.post(reverse("api:create_menu"), data=data)
        status = result.json().get('success')
        self.assertEqual(Menu.objects.count(), 1)
        self.assertEqual(status, True)
        
        
