from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework import status
from home.helperServices import *
from home.models import *
from home.serilaizers import *


# Service to Register employee
class employeeRegistration(APIView):
    def post(self, request):
        data = request.data
        password = data["password"]
        user = User.objects.filter(email=data['email'])
        if user.exists():
            return Response({'status':status.HTTP_400_BAD_REQUEST,'error':'Email already exists'})
        data["role"] = "Employee"
        data["password"] = generate_hash_password(password)
        serializer = UserSerializer(data=data)
        if not serializer.is_valid():
            return Response({'status':status.HTTP_400_BAD_REQUEST,'error':serializer.errors})
        serializer.save()
        token = generate_token(data['email'],data['role'])
        send_verification_mail(data['email'],token)
        return Response({"status":status.HTTP_200_OK,'message':'A verification email is sent to your address please verify yourself'})


# Service to register manager
class managerRegistration(APIView):
    def post(self, request):
        data = request.data
        password = data["password"]
        user = User.objects.filter(email=data['email'])
        if user.exists():
            return Response({'status':status.HTTP_400_BAD_REQUEST,'error':'Email already exists'})
        data["role"] = "Manager"
        data["password"] = generate_hash_password(password)
        serializer = UserSerializer(data=data)
        if not serializer.is_valid():
            return Response({'status':status.HTTP_400_BAD_REQUEST,'error':serializer.errors})
        serializer.save()
        token = generate_token(data['email'],data['role'])
        send_verification_mail(data['email'],token)
        return Response({"status":status.HTTP_200_OK,'message':'A verification email is sent to your address please verify yourself'})


# Service to verify user
@api_view(['GET'])
def verifyUser(request):
    token = request.GET.get('token')
    response = cheack_valid_token(token)
    if not response['valid']:
        return Response({'status':status.HTTP_401_UNAUTHORIZED,'error':response['error']})
    email = response["data"]["email"]
    try:
        obj = User.objects.get(email=email)
        obj.isVerified = True
        obj.save()
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
            token = generate_token(obj.email,obj.role)
        except User.DoesNotExist:
            return Response({'status':status.HTTP_401_UNAUTHORIZED,'error':'Invalid username or password'})
        return Response({'status':status.HTTP_200_OK,'message':'success','data':{'token':token,'role':obj.role}})


    
    


        


      
    