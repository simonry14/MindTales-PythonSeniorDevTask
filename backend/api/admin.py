from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Restaurant)
admin.site.register(Employee)
admin.site.register(Menu)
admin.site.register(Vote)
admin.site.register(User)