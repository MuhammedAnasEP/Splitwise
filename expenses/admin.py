from django.contrib import admin
from .models import User, Expense

# Register your models here.

admin.site.register(User)
admin.site.register(Expense)
