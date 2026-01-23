from django.contrib import admin
from home.models import User,Department,Budget,Expense,ExpenseApproval

# Register your models here.

admin.site.register(User)
admin.site.register(Department)
admin.site.register(Budget)
admin.site.register(Expense)
admin.site.register(ExpenseApproval)