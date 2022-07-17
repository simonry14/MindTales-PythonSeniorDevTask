from rest_framework import serializers
from .models import Employee, Restaurant, Menu, Vote

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ('id', 'name', 'phone_number', 'user')
        
class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ('id', 'name', 'address', 'created_by')
        
class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ('id', 'restaurant', 'file', 'uploaded_at', 'uploaded_by', 'votes')
        
class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ('id', 'employee', 'menu', 'voted_at')