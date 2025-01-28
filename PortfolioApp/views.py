from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from rest_framework import permissions
from .models import *

# Signup API
class SignupAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(email=email).exists():
            return Response({'error': 'Email already registered'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, email=email, password=password)
        token, created = Token.objects.get_or_create(user=user)
        return Response({'message': 'User created successfully', 'token': token.key}, status=status.HTTP_201_CREATED)

# Login API
class LoginAPIView(APIView):
    permission_classes = []
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            request.session["auth_token"] = token.key
            request.session["auth_username"] = username
            return Response({'message': 'Login successful', 'token': token.key}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    
def check_token(token,username):
    user = User.objects.get(username=username)
    try:
        get_token = Token.objects.get(user=user)
    except Token.DoesNotExist:
        return False
    if get_token.key == token:
        return True
    return False




class HomePageView(APIView):
    permission_classes = []
    def get(self,request,*args,**kwargs):
        try:
            token,username = request.session.get('auth_token'),request.session.get('auth_username')
            if not check_token(token,username):
                return Response({"message":"Invalid Credentials"})
            return render(request,'C:/Users/SAGAR/OneDrive/Desktop/Projects/Portfolio/PortfolioApp/templates/home.html')
        except Exception as err:
            return Response({"error":err},status=status.HTTP_500_INTERNAL_SERVER_ERROR)



def auth_page(request):
    return render(request, 'auth.html')

class AddTaskView(APIView):
    permission_classes = []
    def post(self,request,*args,**kwargs):
        token,username = request.session.get('auth_token'),request.session.get('auth_username')
        if not check_token(token,username):
            return Response({"message":"Invalid Credentials"})
        try:
            title = request.data.get("task")
            if title:
                ToDoModel.objects.create(title=title)

        except Exception as err:
            print(err)
        tasks = ToDoModel.objects.all()
        return render(request,'C:/Users/SAGAR/OneDrive/Desktop/Projects/Portfolio/PortfolioApp/templates/todolist.html',{"tasks":tasks})
    
    def get(self,request,*args,**kwargs):
        token,username = request.session.get('auth_token'),request.session.get('auth_username')
        if not check_token(token,username):
            return Response({"message":"Invalid Credentials"})
        tasks = ToDoModel.objects.all()
        return render(request,'C:/Users/SAGAR/OneDrive/Desktop/Projects/Portfolio/PortfolioApp/templates/todolist.html',{"tasks":tasks})
    




