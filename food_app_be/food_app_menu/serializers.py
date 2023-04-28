from food_app_menu.models import *
from rest_framework import serializers


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['id','name','description','address','phone_number','logo','user_id']
    
    def create(self,validated_data):
        """
        Create and return a new `Restaurant` instance, given the validated data.
        """
        return Restaurant.objects.create(**validated_data)
    

    def update(self, instance, validated_data):
        """
        Update and return an existing `Restaurant` instance, given the validated data.
        """
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.address = validated_data.get('address', instance.address)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.logo = validated_data.get('logo', instance.logo)
        instance.save()
        return instance
    
class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ['id','name','description','restaurant_id']

    def create(self,validated_data):
        """
        Create and return a new `Menu instance, given the validated data.
        """
        return Menu.objects.create(**validated_data)
    

    def update(self, instance, validated_data):
        """
        Update and return an existing `Menu` instance, given the validated data.
        """
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance
    
class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ['id','name','description','price','menu_id']

    def create(self,validated_data):
        """
        Create and return a new `MenuItem` instance, given the validated data.
        """
        return MenuItem.objects.create(**validated_data)
    

    def update(self, instance, validated_data):
        """
        Update and return an existing `MenuItem` instance, given the validated data.
        """
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.price = validated_data.get('price',instance.price)
        instance.save()
        return instance
    
    
class CartItemSerializer(serializers.ModelSerializer):
    item_id = serializers.IntegerField(source='menuitem.id')
    class Meta:
        model = CartItem
        fields = ('id','item_id','item_name','quantity', 'cost','cart_id')

class CartItemSerializer2(serializers.ModelSerializer):
    item_id = serializers.IntegerField(source='item.id')
    item = MenuItemSerializer()
    class Meta:
        model = CartItem
        fields = '__all__'

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, write_only=True)

    class Meta:
        model = Cart
        fields = ('id', 'total_cost', 'date_created', 'user', 'status', 'items','user_id')

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        cart = Cart.objects.create(**validated_data)

        for item_data in items_data:
            item_id = item_data.pop('menuitem')['id']
            item_data['item'] = MenuItem.objects.get(id=item_id)
            item = CartItem.objects.create(cart=cart, item = item_data['item'],item_name =item_data['item_name'],quantity = item_data['quantity'],cost = item_data['cost'])
            item.save()
        return cart
    
    def update(self,instance,validated_data):
        # if 'status' in validated_data:
        #     # check if the status is already updated
        #     if instance.status != validated_data['status']:
        #         raise serializers.ValidationError("Status can only be updated once.")
            
        instance.status = validated_data.get('status',instance.status)
        instance.save()
        return instance





