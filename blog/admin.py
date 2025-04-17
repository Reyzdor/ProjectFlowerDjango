from django.contrib import admin

from .models import Category, Flowers, Order, OrderTime, Basket

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

@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    ...

