from rest_framework import generics,status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,AllowAny
from food_app_users.serializers import *
from food_app_users.models import *
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from django.contrib.auth import get_user_model


class RegisterAPI(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        if serializer.is_valid():
            user = serializer.save()
            if user:
                data = serializer.data
        return Response(data=data, status=status.HTTP_201_CREATED)




##################################### DONT TOUCH BELOW ############################################


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)



class LogoutAPIView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = LogoutSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Invalidate the refresh token
        refresh_token = serializer.validated_data['refresh']
        token = RefreshToken(refresh_token)
        token.blacklist()

        # Return success response
        return Response({'detail': 'Successfully logged out.'}, status=status.HTTP_200_OK)

