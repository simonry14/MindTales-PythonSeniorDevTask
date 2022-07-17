from django.urls import path, re_path
from .views import *
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework import permissions

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [

    path('employees', EmployeeList.as_view()),
    path('create_employee', CreateEmployee.as_view()),
    path('restaurants', RestaurantList.as_view()),
    path('create_restaurant', CreateRestaurant.as_view()),
    path('create_menu', CreateMenu.as_view()),
    path('menus', MenuList.as_view()),
    path('today-menus', TodayMenuList.as_view()),
    path('vote', VoteView.as_view()),
    path('register', RegisterView.as_view()),
    path('login', LoginView.as_view()),
    path('results',CurrentResultsView.as_view()),
    path('api-token-auth', obtain_auth_token, name='api_token_auth'),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]