from django.shortcuts import render
from django.db.models import Q

from .models import Restaurant, Employee, Menu, Vote, User
from .serializers import RestaurantSerializer, EmployeeSerializer, MenuSerializer, VoteSerializer

from django.forms.models import model_to_dict
from django.contrib.auth import authenticate

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token

from datetime import datetime

# Create your views here.

class RegisterView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        try:
            email = request.data['email']
            username = request.data['username']
            password = request.data['password']
            userExists = User.objects.filter(username=username).exists()
            if userExists:
                return Response({'errors' : ['User already exists']})

            user = User.objects.create_user(username, email, password)
            user.save()
            return Response(model_to_dict(user, ['username', 'email']))

        except:
            return Response({'errors' : ['Some Parameters are Missing: email, username, password are all required']})
        
class LoginView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        try:
            username = request.data['username']
            password = request.data['password']
            user = User.objects.get(username=username)
            if user.check_password(password):
                user = authenticate(request, username=username, password=password)
                token = Token.objects.create(user=user)
                return Response({'token' : model_to_dict(token, ['key', 'created'])})
                #return Response(model_to_dict(user, ['username', 'email']))
            else:
                return Response({'errors' : ['Invalid Password']})
        except:
            return Response({'errors' : ['Invalid Username']})

class RestaurantList(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        restaurants = Restaurant.objects.all()
        serializer = RestaurantSerializer(restaurants, many=True)
        return Response(serializer.data)
    
class CreateRestaurant(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        restaurant = Restaurant(name=request.data['name'], address=request.data['address'], created_by=request.user)
        restaurant.save()
        return Response(model_to_dict(restaurant, ['id', 'name']),status=status.HTTP_201_CREATED)


class CreateMenu(APIView):
    """Create a new menu for a restaurant"""
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        """Create a new menu for a restaurant"""

        restaurant = request.data['restaurant']
        if Menu.objects.filter(restaurant__id=restaurant.id, uploaded_at__date=datetime.now().date()).exists():
            res = {"msg": 'Restaurant already has menu uploaded for the day', "data": None, "success": False}
            return Response(data=res, status=status.HTTP_200_OK)
        else:   
            menu = Menu(restaurant=Restaurant.objects.get(id=request.data['restaurant']), file=request.data['file'], uploaded_by=request.user)
            menu.save()
            return Response(model_to_dict(menu, ['id', 'name']),status=status.HTTP_201_CREATED)


class EmployeeList(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        employees = Employee.objects.all()
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data)

class MenuList(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        menus = Menu.objects.all()
        serializer = MenuSerializer(menus, many=True)
        return Response(serializer.data)
    
class TodayMenuList(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        menus = Menu.objects.filter(uploaded_at__date=datetime.now().date())
        serializer = MenuSerializer(menus, many=True)
        return Response(serializer.data)
        
    
class VoteView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        
        user = request.user
        employee = Employee.objects.get(user=user)
        
        if request.headers['Accept-Version'] == '1.0':
            menu_id = request.data['menu_id']
            menu = Menu.objects.get(id=menu_id)
            if Vote.objects.filter(employee__id=employee.id, voted_at__date=datetime.now().date(), menu__id=menu_id).exists():
                res = {"msg": 'You have already voted today!', "data": None, "success": False}
                return Response(data=res, status=status.HTTP_200_OK)
            else:
                new_vote = Vote.objects.create(employee=employee, menu=menu)
                menu.votes += 1
                menu.save()
                
                qs = Menu.objects.filter(Q(uploaded_at__date=datetime.now().date()))
                serializer = MenuSerializer(qs, many=True)
                res = {
                    "msg": 'Thank you for voting!',
                    "data": serializer.data,
                    "success": True}
                return Response(data=res, status=status.HTTP_200_OK)
        elif request.headers['Accept-Version'] == '1.1':
            menu_ids = request.data['menu_ids']
            for c,menu_id in enumerate(menu_ids):
                menu = Menu.objects.get(id=menu_id)
                if Vote.objects.filter(employee__id=employee.id, voted_at__date=datetime.now().date(), menu__id=menu_id).exists():
                    res = {"msg": 'You have already voted today!', "data": None, "success": False}
                    return Response(data=res, status=status.HTTP_200_OK)
                else:
                    new_vote = Vote.objects.create(employee=employee, menu=menu)
                    menu.votes += (3-c)
                    menu.save()
            qs = Menu.objects.filter(Q(uploaded_at__date=datetime.now().date()))
            serializer = MenuSerializer(qs, many=True)
            res = {
                    "msg": 'Thank you for voting!',
                    "data": serializer.data,
                    "success": True}
            return Response(data=res, status=status.HTTP_200_OK)
                
class CurrentResultsView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        menu = Menu.objects.filter(uploaded_at__date=datetime.now().date()).order_by('-votes').first()
        serializer = MenuSerializer(menu)
        
        return Response(serializer.data)
              
class CreateEmployee(APIView):   
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        employee = Employee(name=request.data['name'], phone_number=request.data['phone_number'], user=request.user)
        employee.save()
        return Response(model_to_dict(employee, ['id', 'name']),status=status.HTTP_201_CREATED)
    



        
    
