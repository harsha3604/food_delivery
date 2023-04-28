from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from food_app_menu.views import *
urlpatterns = [
    path('',RestaurantList.as_view(),name = 'restaurant_list'),
    path('user/<int:user_id>/',UserRestaurantListAPIView.as_view(),name = 'user_restaurant_list'),
    path('create/',RestaurantCreate.as_view(),name = 'restaurant_create'),
    path('<int:id>/',RestaurantDetail.as_view(),name = 'restaurant_detail'),
    path('<int:id>/update/',RestaurantUpdate.as_view(),name = 'restaurant_update'),

########################## MENU ##################################################################
    path('<int:restaurant_id>/menu/',MenuList.as_view(),name = 'menu_list'),
    path('<int:restaurant_id>/menu/create/',MenuCreate.as_view(),name = 'menu_create'),
    path('<int:restaurant_id>/menu/<int:menu_id>/',MenuUpdate.as_view(),name = 'menu_update'),

################################### MENULIST ######################################################
    path('<int:restaurant_id>/menu/items/',MenuItemList.as_view(),name = 'menu_item_list'),
    path('<int:restaurant_id>/menu/<int:menu_id>/create/',MenuItemCreate.as_view(),name = 'menu_item_create'),
    path('<int:restaurant_id>/menu/items/<int:pk>/',MenuItemUpdate.as_view(),name = 'menu_item_update'),

################################### CART + CARTITEMS ##############################################
    path('user/<int:user_id>/cartitem/create/',CartItemCreate.as_view(),name = 'cart_item_create'),
    path('user/<int:user_id>/cart/create/',CartCreate.as_view(),name = 'cart_create'),
    path('user/<int:user_id>/cart/view/',CartList.as_view(),name='cart_list'),
    path('user/<int:user_id>/cartitems/view/',CartItemList.as_view(),name = 'cart_tem_list'),
    path('user/cart/<int:pk>/update/',CartUpdate.as_view(),name = 'cart_update'),
    path('user/<int:user_id>/cart_owner/',PerUserCartList.as_view(),name='cart_list_owner'),
    path('allcartitems/',AllCartItems.as_view(),name='all_cartitems'),
]
