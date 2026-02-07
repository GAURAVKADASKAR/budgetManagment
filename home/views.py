from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework import status
from home.helperServices import *
from home.models import *
from home.serilaizers import *
from django.utils import timezone
from django.db.models import Sum 


# Service to Register employee
class employeeRegistration(APIView):
    def post(self, request):
        data = request.data
        password = data["password"]
        user = User.objects.filter(email=data['email'])
        if user.exists():
            return Response({'status':status.HTTP_400_BAD_REQUEST,'message':'Email already exists'})
        data["role"] = "Employee"
        data["password"] = generate_hash_password(password)
        serializer = UserSerializer(data=data)
        if not serializer.is_valid():
            return Response({'status':status.HTTP_400_BAD_REQUEST,'message':serializer.errors})
        user=serializer.save()
        userLogObj = {
            'loginUser' : user.userId,
            'email' : user.email,
            'action' :request.path,
            'actionType' : request.method,
            'message' : f'A verification email is sent to user : {user.userId}',
            'ipAddress' : request.META.get('REMOTE_ADDR'),
            'statusCode' : status.HTTP_200_OK
        }
        serializer = UserLogSerializer(data=userLogObj)
        if not serializer.is_valid():
            return Response({'status':status.HTTP_400_BAD_REQUEST,'message':serializer.errors})
        serializer.save()
        token = generate_token(data['email'],data['role'],user.userId)
        send_verification_mail(data['email'],token)
        return Response({"status":status.HTTP_200_OK,'message':'A verification email is sent to your address please verify yourself'})


# Service to register manager
class managerRegistration(APIView):
    def post(self, request):
        data = request.data
        password = data["password"]
        user = User.objects.filter(email=data['email'])
        if user.exists():
            return Response({'status':status.HTTP_400_BAD_REQUEST,'message':'Email already exists'})
        data["role"] = "Manager"
        data["password"] = generate_hash_password(password)
        serializer = UserSerializer(data=data)
        if not serializer.is_valid():
            return Response({'status':status.HTTP_400_BAD_REQUEST,'message':serializer.errors})
        user = serializer.save()
        userLogObj = {
            'loginUser' : user.userId,
            'email' : user.email,
            'action' :request.path,
            'actionType' : request.method,
            'message' : f'A verification email is sent to user : {user.userId}',
            'ipAddress' : request.META.get('REMOTE_ADDR'),
            'statusCode' : status.HTTP_200_OK
        }
        serializer = UserLogSerializer(data=userLogObj)
        if not serializer.is_valid():
            return Response({'status':status.HTTP_400_BAD_REQUEST,'message':serializer.errors})
        serializer.save()
        token = generate_token(data['email'],data['role'],user.userId)
        send_verification_mail(data['email'],token)
        return Response({"status":status.HTTP_200_OK,'message':'A verification email is sent to your address please verify yourself'})


# Service to verify user
@api_view(['GET'])
def verifyUser(request):
    token = request.GET.get('token')
    response = cheack_valid_token(token)
    if not response['valid']:
        return Response({'status':status.HTTP_401_UNAUTHORIZED,'message':response['error']})
    email = response["data"]["email"]
    try:
        obj = User.objects.get(email=email)
        obj.isVerified = True
        obj.save()
        userLogObj = {
            'loginUser' : obj.userId,
            'email' : obj.email,
            'action' :request.path,
            'actionType' : request.method,
            'message' : f'user has been verified : {obj.userId}',
            'ipAddress' : request.META.get('REMOTE_ADDR'),
            'statusCode' : status.HTTP_200_OK
        }
        serializer = UserLogSerializer(data=userLogObj)
        if not serializer.is_valid():
            return Response({'status':status.HTTP_400_BAD_REQUEST,'message':serializer.errors})
        serializer.save()
    except User.DoesNotExist:
        return Response({'status':status.HTTP_404_NOT_FOUND,'message':'invalid email'})
    return Response({'status':status.HTTP_200_OK,'message':'successfully verified'})

# Service to login user
class loginUser(APIView):
    def post(self,request):
        data = request.data
        email = data['email']
        password = data['password']
        hashPassword = generate_hash_password(password)
        try:
            obj = User.objects.get(email=email,password=hashPassword)
            token = generate_token(obj.email,obj.role,obj.userId)
        except User.DoesNotExist:
            return Response({'status':status.HTTP_401_UNAUTHORIZED,'message':'Invalid username or password'})
        return Response({'status':status.HTTP_200_OK,'message':'login successfully','data':{'token':token,'role':obj.role}})

# Service to create Budget
class createBudget(APIView):
    def post(self,request):
        data = request.data
        role = request.role
        userId = request.userId
        if role=="Manager":
            data['createdByUser'] = userId
            serializer = BudgetSerializer(data=data)
            if not serializer.is_valid():
                return Response({"status":status.HTTP_400_BAD_REQUEST,'message':serializer.errors})
            serializer.save()
            return Response({'status':status.HTTP_200_OK,'message':'Budget Created'})
        return Response({'status':status.HTTP_401_UNAUTHORIZED,'message':'Invalid permission'})
    
# Service to List all budget
class getBudget(APIView):
    def get(self,request):
        budgetId = request.GET.get("budgetId")
        if budgetId:
            budget = Budget.objects.filter(budgetId=budgetId,endDate__isnull=True,status="Active")
        else:
            budget = Budget.objects.filter(endDate__isnull=True,status="Active")
        serializer = BudgetSerializer(budget,many=True)
        return Response({'status':status.HTTP_200_OK,'message':'success','data':serializer.data})

# service to update Budget
class updateBudget(APIView):
    def patch(self,request,budgetId):
        role = request.role
        userId = request.userId
        if role=="Manager":
            try:
                budget = Budget.objects.get(budgetId=budgetId,createdByUser=userId)
            except Budget.DoesNotExist:
                return Response({'status':status.HTTP_404_NOT_FOUND,'message':'Invalid Budget ID or you did not create this budget'})
            serializer = BudgetSerializer(budget,data=request.data,partial=True)
            if not serializer.is_valid():
                return Response({'status':status.HTTP_400_BAD_REQUEST,'message':serializer.errors})
            serializer.save()
            return Response({'status':status.HTTP_200_OK,'message':'Budget updated'})
        else:
            return Response({'status':status.HTTP_401_UNAUTHORIZED,'message':'Invalid Permission'})
    
# Service to delete budget
class deleteBudget(APIView):
    def patch(self,request,budgetId):
        role = request.role
        userId = request.userId
        if role=="Manager":
            try:
                budget = Budget.objects.get(budgetId=budgetId,createdByUser=userId)
            except Budget.DoesNotExist:
                return Response({'status':status.HTTP_404_NOT_FOUND,'message':'Invalid Budget ID or you did not create this budget'})
            budget.endDate = timezone.now()
            budget.status="Closed"
            budget.save()
            return Response({'status':status.HTTP_200_OK,'message':'Budget deleted'})
        else:
            return Response({'status':status.HTTP_401_UNAUTHORIZED,'message':'Invalid Permission'})

# Service to create Expense
class CreateExpense(APIView):
    def post(self,request):
        data = request.data.copy()
        userId = request.userId
        assignedManager = data.pop('assignedManager')
        data['submittedByUserId']=userId
        expenseSerailzer = ExpenseSerializer(data=data)
        if not expenseSerailzer.is_valid():
            return Response({'status':status.HTTP_400_BAD_REQUEST,'message':expenseSerailzer.errors})
        expense=expenseSerailzer.save()
        expenseApproval = {
            'expenseId': expense.expenseId,
            'assignedUser': assignedManager
        }
        expenseApprovalSerializer = ExpenseApprovalSerializer(data=expenseApproval)
        if not expenseApprovalSerializer.is_valid():
            return Response({'status':status.HTTP_400_BAD_REQUEST,'message':expenseApprovalSerializer.errors})
        expenseObj=expenseApprovalSerializer.save()
        notification = Notification.objects.create(
            toUserId=expenseObj.assignedUser,
            type="Expense Approval Pending",
            message=(
                f"An expense request of ₹{expense.amount} "
                f"has been submitted and is awaiting your approval."
            )
        )
        notification.save()
        return Response({'status':status.HTTP_200_OK,'message':'Expense created'})

# Service to update Expense 
class updateExpense(APIView):
    def patch(self,request,expenseId):
        userId = request.userId
        try:
            expense = Expense.objects.get(expenseId=expenseId,submittedByUserId=userId)
        except Expense.DoesNotExist:
            return Response({'status':status.HTTP_404_NOT_FOUND,'message':'Invalid expense ID or you did not create this expense'})
        serializer = ExpenseSerializer(expense,data=request.data,partial=True)
        if not serializer.is_valid():
            return Response({'status':status.HTTP_400_BAD_REQUEST,'message':serializer.errors})
        serializer.save()
        return Response({'status':status.HTTP_200_OK,'Expense Updated':'success'})

# Service to delete Expense
class deleteExpense(APIView):
    def patch(self,request,expenseId):
        userId = request.userId
        try:
            expense = Expense.objects.get(expenseId=expenseId,submittedByUserId=userId,endDate__isnull=True)
        except Expense.DoesNotExist:
            return Response({'status':status.HTTP_404_NOT_FOUND,'message':'Invalid expense ID or you did not create this expense'})
        expense.endDate=timezone.now()
        expense.save()
        return Response({'status':status.HTTP_200_OK,'message':'Expense Deleted'})

# Service to get exppenses
class getExpense(APIView):
    def get(self,request):
        expenseId = request.GET.get("expenseId")
        if expenseId:
            expense = Expense.objects.filter(expenseId=expenseId,endDate__isnull=True)
        else:
            expense = Expense.objects.filter(endDate__isnull=True)
        serializer = ExpenseSerializer(expense,many=True)
        return Response({'status':status.HTTP_200_OK,'message':'success','data':serializer.data})


# Service to approve expense
class approveExpense(APIView):
    def patch(self,request,expenseId):
        userId = request.usreId
        try:
            expense = ExpenseApproval.objects.get(expenseId=expenseId,assignedUser=userId)
        except ExpenseApproval.DoesNotExist:
            return Response({'status':status.HTTP_404_NOT_FOUND,'message':'Unable to find expense'})
        expenseObj = Expense.objects.get(expenseId=expenseId)
        expenseObj.status="Approved"
        expenseObj.endDate = timezone.now()
        expenseObj.save()
        notification = Notification.objects.create(
            message = f"Your expense request of ₹{expenseObj.amount} has been approved by the manager.",
            toUserId = expenseObj.submittedByUserId,
            type = "Approval"
        )
        notification.save()
        return Response({'status':status.HTTP_200_OK,'message':f'Expense Approved {expenseId}'})

# Service to Reject expense
class rejectExpense(APIView):
    def patch(self,request,expenseId):
        userId = request.userId
        try:
            expense = ExpenseApproval.objects.get(expenseId=expenseId,assignedUser=userId)
        except ExpenseApproval.DoesNotExist:
            return Response({'status':status.HTTP_404_NOT_FOUND,'message':'Unable to find expense'})
        expenseObj = Expense.objects.get(expenseId=expenseId)
        expenseObj.status="Rejected"
        expenseObj.endDate = timezone.now()
        expenseObj.save()
        notification = Notification.objects.create(
            message = f"Your expense request of ₹{expenseObj.amount} has been Rejected by the manager.",
            toUserId = expenseObj.submittedByUserId,
            type = "Reject"
        )
        notification.save()
        return Response({'status':status.HTTP_200_OK,'message':f'Expense Rejected {expenseId}'})

# Service to get notification
class getnotification(APIView):
    def get(self,request):
        notificationId = request.GET.get("notificationId")
        userId = request.userId
        if notificationId:
            notification = Notification.objects.filter(notificationId=notificationId,toUserId=userId,status="Unread")
        else:
            notification = Notification.objects.filter(toUserId=userId,status="Unread")
        serializer = NotificationSerializer(notification,many=True)
        return Response({'status':status.HTTP_200_OK,'message':'success','data':serializer.data})

# Service to update notification read status
class markNotificationAsRead(APIView):
    def patch(self,request,notificationId):
        userId = request.userId
        try:
            notification = Notification.objects.get(notificationId=notificationId,toUserId=userId)
        except Notification.DoesNotExist:
            return Response({'status':status.HTTP_404_NOT_FOUND,'message':'Invalid request'})
        notification.status = "Read"
        notification.save()
        return Response({'status':status.HTTP_200_OK,'message':'success'})


# Service to generate budget utilization
class budgetUtilizationReport(APIView):
    def get(self,request,budgetId):
        reminingAmount =  0
        overBudgetAmount = 0
        healthStatus = "Ok"
        role = request.role
        if role != "Admin":
            expenseTotal = Expense.objects.filter(relatedBudgetId=budgetId,status="Approved").aggregate(total=Sum("amount"))["total"] or 0
            budget = Budget.objects.filter(budgetId=budgetId).first()
            if not budget:
                return Response({'status':status.HTTP_404_NOT_FOUND,'message':'Budget not found'})   
            budgetTotal = budget.amountAllocated
            if expenseTotal>budgetTotal:
                overBudgetAmount=expenseTotal-budgetTotal
            else:
                reminingAmount = budgetTotal-expenseTotal
            utilization = (expenseTotal / budgetTotal)*100
            if utilization>100:
                healthStatus = "EXCEEDED"
            elif utilization >=80:
                healthStatus = "WARNING"
            return Response({'status': status.HTTP_200_OK,'data':{
                'expenseTotal':expenseTotal,
                'budgetTotal':budgetTotal,
                'raminingAmount':reminingAmount,
                'overBudgetAmount':overBudgetAmount,
                'utilization':utilization,
                'healthStatus':healthStatus
            },
            'message':f'Report for budget : {budgetId} is succefully created'})
        else:
            return Response({'status':status.HTTP_401_UNAUTHORIZED,'message':'permission denied'})    
    

