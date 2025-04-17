from django.contrib import admin

<<<<<<< HEAD
from .models import Category, Flowers, Order, OrderTime, Basket
=======
from .models import User, Category, Flowers, Order, OrderTime, Basket


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    ...
>>>>>>> 3741d9c (Update HTML + flower_detail + interface)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    ...

@admin.register(Flowers)
class FlowersAdmin(admin.ModelAdmin):
    ...

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    ...

@admin.register(OrderTime)
class OrderTimeAdmin(admin.ModelAdmin):
    ...

<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> 3741d9c (Update HTML + flower_detail + interface)
@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    ...

<<<<<<< HEAD
=======
>>>>>>> ad7377b (Update HTML + images + interface)
=======
>>>>>>> 3741d9c (Update HTML + flower_detail + interface)
