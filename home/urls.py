"""
URL configuration for budgetManagement project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from home.views import *

urlpatterns = [
    path('employee/register/',employeeRegistration.as_view()),
    path('manager/register/',managerRegistration.as_view()),
    path('verify/',verifyUser),
    path('login/',loginUser.as_view()),
    path('createBudget/',createBudget.as_view()),
    path('GetAllBudget/',getBudget.as_view()),
    path('updateBudget/<int:budgetId>/',updateBudget.as_view()),
    path('deleteBudget/<int:budgetId>/',deleteBudget.as_view()),
    path('CreateExpense/',CreateExpense.as_view()),
    path('updateExpense/<int:expenseId>/',updateExpense.as_view()),
    path('getExpense/',getExpense.as_view()),
    path('approveExpense/<int:expenseId>/',approveExpense.as_view()),
    path('rejectExpense/<int:expenseId>/',rejectExpense.as_view()),
    path('getnotification/',getnotification.as_view()),
    path('markNotificationAsRead/<int:notificationId>/',markNotificationAsRead.as_view())
]