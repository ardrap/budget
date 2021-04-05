from django.db import models
from django.contrib.auth.models import User

# Create your models here.

#create entry,update,delete
#category
#expenses(data,category,amount,notes,user)
class Category(models.Model):
    category_name=models.CharField(max_length=120,unique=True)

    def __str__(self):
        return self.category_name

class Expense(models.Model):
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    notes=models.CharField(max_length=250,null=True)
    amount=models.IntegerField()
    user=models.CharField(max_length=120)
    date=models.DateField()

    def __str__(self):
        return self.user

#template inheritance
#django user authentication(registration,login,logout)
#
#
