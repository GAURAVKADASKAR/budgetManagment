from home.views import *
from rest_framework.response import Response as DRFResponse
from django.http import JsonResponse
class AuthLoggingMiddleware:
    def __init__(self,get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        if (not request.path.startswith('/api/')):
            return self.get_response(request)
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        token = None
        if auth_header.startswith('Bearer '):
            token = auth_header.split()[1]
        if not token:
            return JsonResponse({'status':status.HTTP_401_UNAUTHORIZED,'message':'token missing'})
        response = cheack_valid_token(token)
        if not response['valid']:
            return JsonResponse({'status':status.HTTP_401_UNAUTHORIZED,'error':response['error']})
        email = response["data"]["email"]
        userId = response['data']['userId']
        request.email = email
        request.userId = userId
        request.role = response['data']['role']
        user_obj = User.objects.get(userId=userId)
        response = self.get_response(request)
        UserLog.objects.create(
            loginUser = user_obj,
            email = email,
            action = request.path,
            actionType = request.method,
            message = response.data.get('message'),
            ipAddress =request.META.get('REMOTE_ADDR'),
            statusCode = response.data.get('status')
        )
        return response
        