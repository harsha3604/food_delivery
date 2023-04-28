from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from rest_framework_simplejwt.tokens import RefreshToken
from food_app_users.roles import *
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.contrib.auth.models import PermissionsMixin


class UserManager(BaseUserManager):
    def _create_user(self, username, email, password, **extra_fields):
        """
        Creates and saves a User with the given username, email and password
        """
        if not username:
            raise ValueError('Users must have an username')
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

    def create_user(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, password, **extra_fields)
    
class MainUser(AbstractBaseUser,PermissionsMixin):
    username = models.CharField(max_length=30,unique=True)
    email = models.CharField(max_length=100,blank=False,unique=True)
    first_name = models.CharField(max_length=40, blank=True)
    last_name = models.CharField(max_length=40, blank=True)
    date_joined = models.DateTimeField(default=timezone.now)
    role = models.CharField(max_length=30,choices = USER_ROLE_CHOICES, blank=False, null=False, default=CUSTOMER)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']


    def __str__(self):
        return self.username


    def role_indexing(self):
        if self.role == 1:
            return 'Owner'
        elif self.role == 2:
            return 'Customer'
        

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return{
            'refresh':str(refresh),
            'access':str(refresh.access_token)}
    
    class Meta:
        '''
        to set table name in database
        '''
        db_table = "User"


