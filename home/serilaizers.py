from rest_framework import serializers
from home.models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

# Serializer for budget
class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = '__all__'
    
#  Serializer for expense
class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = '__all__'


# Serializer for ExpenseApproval
class ExpenseApprovalSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseApproval
        fields = '__all__'

# Serializer for Notification
class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'
    
# Serializer for User log's
class UserLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLog
        fields = '__all__'
    
