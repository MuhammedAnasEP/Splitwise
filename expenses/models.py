from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=15)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.name
    
class Expense(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_by = models.ForeignKey(User,on_delete=models.CASCADE)
    split_type = models.CharField(max_length=10)
    participants = models.ManyToManyField(User,related_name='expenses_participated')
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)