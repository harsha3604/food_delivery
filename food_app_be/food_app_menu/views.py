from food_app_menu.models import *
from food_app_menu.serializers import *
from rest_framework.response import Response
from rest_framework import status,generics,viewsets
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.decorators import action

class RestaurantList(generics.ListAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [IsAuthenticated]

class UserRestaurantListAPIView(generics.ListAPIView,LoginRequiredMixin):
    serializer_class = RestaurantSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Restaurant.objects.filter(user_id=user_id)


class RestaurantCreate(generics.ListCreateAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        if isinstance(user, MainUser):
            serializer.save(user=user)
        else:
            raise ValueError("Authenticated user must be a MainUser instance.")


class RestaurantDetail(generics.RetrieveAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

class RestaurantUpdate(generics.RetrieveUpdateDestroyAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

########################################################### MENU ###################################################################
class MenuList(generics.ListAPIView):
    serializer_class = MenuSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        restaurant_id = self.kwargs['restaurant_id']
        return Menu.objects.filter(restaurant_id=restaurant_id)


class MenuCreate(generics.CreateAPIView):
    serializer_class = MenuSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, restaurant_id):
        restaurant = Restaurant.objects.get(pk=restaurant_id)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(restaurant=restaurant)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class MenuUpdate(generics.RetrieveUpdateDestroyAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        restaurant_id = self.kwargs['restaurant_id']
        menu_id = self.kwargs['menu_id']
        obj = get_object_or_404(Menu, pk=menu_id, restaurant_id=restaurant_id)
        return obj


########################################################### MENU ITEM ###################################################################


class MenuItemList(generics.ListAPIView):
    serializer_class = MenuItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        restaurant_id = self.kwargs['restaurant_id']
        return MenuItem.objects.filter(menu__restaurant__id = restaurant_id)


class MenuItemCreate(generics.CreateAPIView):
    serializer_class = MenuItemSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, menu_id,restaurant_id):
        menu = Menu.objects.get(pk= menu_id)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(menu = menu)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class MenuItemUpdate(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [IsAuthenticated]

########################################################### CART AND CART ITEM ###################################################################

class CartItemCreate(generics.CreateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

class CartCreate(generics.CreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        # Get the currently logged in user
        user = request.user

        # Set the user_id field in the validated data
        validated_data = {**self.request.data, "user_id": user.id}
        # Create the cart object using the modified validated data
        serializer = self.get_serializer(data=validated_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        # Return the serialized data for the created cart object
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
class CartList(generics.ListAPIView):
    serializer_class = CartSerializer
    permission_classes=[IsAuthenticated]

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Cart.objects.filter(user_id = user_id)
    
class CartItemList(generics.ListAPIView):
    serializer_class=CartItemSerializer2
    permission_classes=[IsAuthenticated]

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return CartItem.objects.filter(cart__user__id = user_id)
    

class CartUpdate(generics.UpdateAPIView):
    serializer_class = CartSerializer
    permission_classes=[IsAuthenticated]
    queryset = Cart.objects.all()
    lookup_field = 'pk'

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid()
        serializer.save(status=request.data.get('status'))
        return Response(serializer.data)



class PerUserCartList(generics.ListAPIView):
    serializer_class = CartSerializer

    def get_queryset(self):
        # Get the user ID from the request parameters
        user_id = self.kwargs['user_id']
        print(user_id)
        # Query all cart items belonging to menus of restaurants belonging to the user
        queryset = Cart.objects.filter(
            cartitem__item__menu__restaurant__user_id=user_id
        ).distinct()

        return queryset
    
class AllCartItems(generics.ListAPIView):
    serializer_class = CartItemSerializer2
    permission_classes=[IsAuthenticated]
    queryset=CartItem.objects.all()