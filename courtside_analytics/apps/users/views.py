from django.shortcuts import render
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import CustomUser
from .serializers import (UserSerializer, RegisterSerializer, LoginSerializer)

# Create your views here.
class RegisterView(generics.CreateAPIView):
    # POST/api/auth/register/
    # allows anyone to create a new user account

    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny] # anyone is allowed to register

    def create(self, request, *args, **kwargs):
        # after creating the user, auto-login or return user data

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save() # calls serializer's create method

        #return the created user excluding password
        return Response(
            UserSerializer(user).data,
            status=status.HTTP_201_CREATED
        )


class LoginView(APIView):
    # POST/api/auth/login/
    # accepts email and password, returns JWT tokens if credentials are valid

    permission_classes = [permissions.AllowAny] # anyone can login

    def post(self, request):
        print("Login request data:", request.data)

        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():

            #get the authenticated user from serializer
            user = serializer.validated_data['user']

            #generate JWT tokens
            # GET/api/auth/refresh/
            refresh = RefreshToken.for_user(user)

            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserSerializer(user).data
            }, status=status.HTTP_200_OK)

        print("Validation errors:", serializer.errors)
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

class UserProfileView(generics.RetrieveUpdateAPIView):
    # GET/api/users/me/ is for profile view
    # PUT/api/users/me/ is for updating profile
    # only authenticated users can access their own profile

    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # return the currently logged in user
        # ensures users can only see or update their own profile

        return self.request.user