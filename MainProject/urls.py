from django.contrib import admin
<<<<<<< HEAD
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from blog.views import *

urlpatterns = [
    path('', index, name='index'),
    path('admin/', admin.site.urls),
    path('flower/<int:flower_id>/', flower_id, name='flower_detail'),
    path('login/', login_view, name='login'),  
    path('registration/', reg_view, name='registration'),  
    path('logout/', logout, name='logout'), 
    path('basket/', basket, name='basket'),
    path('add_basket/', add_basket, name='add_basket'),
    path('update_quantity/', update_quantity, name='update_quantity'),
    path('remove_from_basket/<int:item_id>/', remove_from_basket, name='remove_from_basket'),
    path('order/success/<int:order_id>/', order_success, name='order_success'),
    path('process_delivery/', process_delivery, name='process_delivery'), 
    path('complete_order/', complete_order, name='complete_order'),
    path('delivery/', delivery_view, name='delivery'),
    path('logout/', logout_view, name='logout'),
    path('category/<slug:slug>/', category_detail, name='category_detail'),
    path('save-delivery-data/', save_delivery_data, name='save_delivery_data'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
=======
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from blog.views import index
from blog import views

urlpatterns = [      
    path('', index, name='index'),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
>>>>>>> 02e56ac (Commit: Update HTML)
