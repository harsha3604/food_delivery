from rest_framework import serializers
from food_app_users.models import *
from food_app_users.serializers import *
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model

User = get_user_model()



from rest_framework import serializers
from food_app_users.models import *
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model,password_validation

MainUser = get_user_model()



class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type': 'password'})

    class Meta:
        model = MainUser
        fields = ('id', 'username', 'email', 'first_name', 'last_name',
                  'date_joined','role', 'password')
        

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


########################### DONT TOUCH BELOW THIS POINT #########################################################

class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6,write_only=True)
    username = serializers.CharField(max_length=255, min_length=3)
    tokens = serializers.SerializerMethodField()

    def get_tokens(self, obj):
        user = User.objects.get(username=obj['username'])
        return {
            'refresh': user.tokens()['refresh'],
            'access': user.tokens()['access']
        }
    
    class Meta:
        model = User
        fields = ['username','password','tokens','role','id']
    def validate(self, attrs):
        username = attrs.get('username','')
        password = attrs.get('password','')

        user = auth.authenticate(username=username,password=password)
        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact admin')
        return {
            'email': user.email,
            'username': user.username,
            'tokens': user.tokens,
            'role':user.role,
            'id':user.id,
        }

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()