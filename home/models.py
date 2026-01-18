from django.db import models

# Create your models here.

# Model to store Department
class Department(models.Model):
    departmentId = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.TextField(default=True)

    def __str__(self):
        return self.name

# Model for User
class User(models.Model):
    status_choices = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    ]
    role_choices = [
        ('Employee','Employee'),
        ('Manager','Manager'),
        ('Admin','Admin')
    ]
    userId = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    department = models.ForeignKey(Department,on_delete=models.PROTECT)
    status = models.CharField(max_length=10, choices=status_choices, default='Active')
    password = models.CharField(max_length=128)
    isVerified = models.BooleanField(default=False)
    createdDate = models.DateTimeField(auto_now_add=True)
    updatedDate = models.DateTimeField(auto_now=True)
    role = models.CharField(max_length=10,choices=role_choices,default='Employee')

    def __str__(self):
        return self.email

