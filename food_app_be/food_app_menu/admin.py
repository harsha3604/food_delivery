from django.contrib import admin
from food_app_menu.models import *
# Register your models here.

admin.site.register(Restaurant)
admin.site.register(Menu)
admin.site.register(MenuItem)
admin.site.register(Cart)
admin.site.register(CartItem)