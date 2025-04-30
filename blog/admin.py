from django.contrib import admin
from .models import Category, Flowers, Order, OrderTime, Basket

class OrderTimeInline(admin.TabularInline):
    model = OrderTime
    extra = 0  
    readonly_fields = ('get_total',) 
    
    def get_total(self, obj):
        return obj.get_total()
    get_total.short_description = 'Сумма'

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_name', 'phone', 'total_amount', 'status_order', 'created_at', 'display_products')
    list_filter = ('status_order', 'created_at')
    search_fields = ('customer_name', 'phone', 'email', 'address')
    inlines = [OrderTimeInline]
    
    def display_products(self, obj):
        items = OrderTime.objects.filter(order=obj)
        return ", ".join([f"{item.flower.title} ({item.quantity} шт.)" for item in items])
    display_products.short_description = 'Товары в заказе'

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Flowers)
class FlowersAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'stock', 'category')
    list_filter = ('category',)
    search_fields = ('title', 'description')

@admin.register(OrderTime)
class OrderTimeAdmin(admin.ModelAdmin):
    list_display = ('order', 'flower', 'quantity', 'unit_price', 'get_total')
    list_filter = ('order',)
    
    def get_total(self, obj):
        return obj.get_total()
    get_total.short_description = 'Сумма'

@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'created_timestamp')
    list_filter = ('user',)