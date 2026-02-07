from django.contrib import admin
from django.urls import path
from home.views import *

urlpatterns = [
    path('employee/register/',employeeRegistration.as_view()),
    path('manager/register/',managerRegistration.as_view()),
    path('user/verify/',verifyUser),
    path('login/',loginUser.as_view()),
    path('api/budget/create/',createBudget.as_view()),
    path('api/budget/get/',getBudget.as_view()),
    path('api/budget/update/<int:budgetId>/',updateBudget.as_view()),
    path('api/budget/delete/<int:budgetId>/',deleteBudget.as_view()),
    path('api/expense/create/',CreateExpense.as_view()),
    path('api/expense/update/<int:expenseId>/',updateExpense.as_view()),
    path('api/expense/get/',getExpense.as_view()),
    path('api/expense/approve/<int:expenseId>/',approveExpense.as_view()),
    path('api/expense/reject/<int:expenseId>/',rejectExpense.as_view()),
    path('api/notification/get/',getnotification.as_view()),
    path('api/notification/update/read/<int:notificationId>/',markNotificationAsRead.as_view()),
    path('api/report/budget/<int:budgetId>/',budgetUtilizationReport.as_view())
]