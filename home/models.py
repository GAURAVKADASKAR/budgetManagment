from django.db import models
from django.utils import timezone
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

# Model for Budget
class Budget(models.Model):
    status_choices = [
        ('Active','Active'),
        ('Closed','Closed')
    ]
    budgetId = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    Department = models.ForeignKey(Department,on_delete=models.PROTECT)
    amountAllocated = models.PositiveIntegerField()
    startDate = models.DateTimeField(auto_now_add=True)
    endDate = models.DateTimeField(blank=True,null=True)
    status = models.CharField(choices=status_choices,default='Active')
    createdByUser = models.ForeignKey(User,related_name="user",on_delete=models.PROTECT)

    def __str__(self):
        return self.title

# Model for Expense
class Expense(models.Model):
    expense_status = [
        ('Pending','Pending'),
        ('Approved','Approved'),
        ('Rejected','Rejected')
    ]
    expenseId = models.AutoField(primary_key=True)
    relatedBudgetId = models.ForeignKey(Budget,on_delete=models.PROTECT)
    description = models.CharField(max_length=100)
    amount = models.PositiveIntegerField()
    submittedByUserId = models.ForeignKey(User,on_delete=models.PROTECT)
    submittedDate = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10,choices=expense_status,default='Pending')
    updateDate = models.DateTimeField(auto_now=True)
    startDate = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    endDate = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.description

# Model for ExpenseApproval
class ExpenseApproval(models.Model):
    expenseApprovalId = models.AutoField(primary_key=True)
    expenseId = models.ForeignKey(Expense,on_delete=models.CASCADE)
    assignedUser = models.ForeignKey(User,on_delete=models.PROTECT)
    startDate = models.DateTimeField(auto_now_add=True)
    endDate = models.DateTimeField(null=True,blank=True)


# Model for Notification
class Notification(models.Model):
    read_status = [
        ('Unread','Unread'),
        ('Read','Read')
    ]
    notificationId = models.AutoField(primary_key=True)
    toUserId = models.ForeignKey(User,on_delete=models.PROTECT)
    type = models.CharField(max_length=20)
    message = models.TextField()
    status = models.CharField(max_length=10,choices=read_status,default='Unread')
    createDate = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.type
    
# Model to log user activity
class UserLog(models.Model):
    loginUser = models.ForeignKey(User,on_delete=models.PROTECT,related_name='logUser',null=True,blank=True)
    email = models.EmailField(null=True,blank=True)
    action = models.TextField()
    actionType = models.TextField()
    message = models.TextField()
    ipAddress = models.CharField(max_length=100,null=True,blank=True)
    statusCode = models.CharField(max_length=50)
    createdDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.loginUser} - {self.actionType}"
    










