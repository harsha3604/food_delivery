from django.db import models
from food_app_users.models import *
from datetime import datetime
# Create your models here.
class Restaurant(models.Model):
    name = models.CharField(null=True,blank=True,max_length = 100)
    description = models.TextField(null=True,blank=True,max_length = 250)
    address = models.TextField(null=True,blank=True,max_length = 250)
    phone_number = models.IntegerField(null=True,blank=True)
    logo = models.TextField(null=True,blank=True)
    user = models.ForeignKey(MainUser,on_delete=models.CASCADE,null=True,blank=True)

        
    def __str__(self):
        return self.name
    

    
class Menu(models.Model):
    name = models.CharField(null=True,blank=True,max_length = 100)
    description = models.TextField(null=True,blank=True,max_length = 250)
    restaurant = models.ForeignKey(Restaurant,on_delete=models.CASCADE,null = True,blank = True)

    
    def __str__(self):
        return self.name


class MenuItem(models.Model):
    name = models.CharField(null=True,blank=True,max_length = 100)
    description = models.TextField(null=True,blank=True,max_length = 250)
    price = models.IntegerField(null=True,blank=True)
    menu = models.ForeignKey(Menu,on_delete=models.CASCADE,null=True,blank = True)


    def __str__(self):
        return self.name



class Cart(models.Model):
    user = models.ForeignKey(MainUser,on_delete=models.CASCADE)
    total_cost = models.IntegerField(null=False,blank=False,default=0)
    date_created = models.DateTimeField(default=datetime.now)
    status = models.BooleanField(default=False)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart,on_delete = models.CASCADE,null=True,blank=True)
    item = models.ForeignKey(MenuItem,on_delete = models.SET_NULL,null=True,blank=True)
    item_name = models.CharField(null=True,blank=True,max_length = 100)
    quantity = models.IntegerField(null=False,blank=False,default=0)
    price = models.IntegerField(null=False,blank=False,default=0)
    cost = models.IntegerField(null=False,blank=False,default=0)

    def save(self, *args, **kwargs):
        self.item_name = self.item.name
        self.price = self.item.price
        super().save(*args, **kwargs)


