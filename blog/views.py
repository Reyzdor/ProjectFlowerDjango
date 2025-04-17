<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
import json
=======
>>>>>>> 7740582 (Commit: +API Geoapify + OpenStreetMaps new 2 html + address)
from django.db import IntegrityError
from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.urls import reverse
from blog.models import Category, Flowers, Basket, Order, OrderTime
from django.contrib.auth.decorators import login_required  
<<<<<<< HEAD
from django.views.decorators.csrf import csrf_exempt
=======
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
>>>>>>> 02e56ac (Commit: Update HTML)


def logout_view(request):
    messages.get_messages(request).used = True  
    logout(request)
    return redirect('blog/login.html')
=======
from django.shortcuts import render, get_object_or_404, redirect
<<<<<<< HEAD
from django.http import HttpResponse
from django.conf import settings
from blog.models import User, Category, Flowers, Order, OrderTime
>>>>>>> 3741d9c (Update HTML + flower_detail + interface)
=======
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from blog.models import Category, Flowers
>>>>>>> bf0b456 (Commit: +Login +Reg)
=======
>>>>>>> 7740582 (Commit: +API Geoapify + OpenStreetMaps new 2 html + address)

def index(request):
    categories = Category.objects.all()
<<<<<<< HEAD
    flowers = Flowers.objects.all()[:6]  
=======
    flowers = Flowers.objects.all()
<<<<<<< HEAD
<<<<<<< HEAD

>>>>>>> 28078ce (+Js, +btsrp, +html)
=======
    
>>>>>>> 3741d9c (Update HTML + flower_detail + interface)
=======
>>>>>>> bf0b456 (Commit: +Login +Reg)
    context = {
        'categories': categories,
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
        'flowers': flowers,
=======
>>>>>>> 28078ce (+Js, +btsrp, +html)
=======
=======
        'flowers': flowers,
    }
    return render(request, 'blog/index.html', context)

def flower_id(request, flower_id):
    flower = get_object_or_404(Flowers, pk=flower_id)
    additional_flower = Flowers.objects.exclude(id=flower.id).order_by('?').first()
    other_flowers = Flowers.objects.exclude(id=flower.id).order_by('?')[:8]
    context = {
        'flower': flower,
        'additional_flower': additional_flower,
        'other_flowers': other_flowers,
<<<<<<< HEAD
>>>>>>> 3741d9c (Update HTML + flower_detail + interface)
        'SETTINGS': settings,
>>>>>>> 02e56ac (Commit: Update HTML)
    }
<<<<<<< HEAD
    return render(request, 'blog/index.html', context)

<<<<<<< HEAD

def flower_id(request, flower_id):
    flower = get_object_or_404(Flowers, pk=flower_id)
    additional_flower = Flowers.objects.exclude(id=flower.id).order_by('?').first()
    other_flowers = Flowers.objects.exclude(id=flower.id).order_by('?')[:8]
    context = {
        'flower': flower,
        'additional_flower': additional_flower,
        'other_flowers': other_flowers,
    }
=======
    }
>>>>>>> bf0b456 (Commit: +Login +Reg)
    return render(request, 'blog/flower_detail.html', context)

def reg_view(request):
    if request.method == 'POST':
        username = request.POST.get('login')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password != password2:
            messages.error(request, 'Пароли не совпадают')
            return render(request, 'auth/reg.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Пользователь с таким именем уже существует')
            return render(request, 'auth/reg.html')

        try:
            user = User.objects.create_user(username=username, password=password)
            auth_login(request, user)
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('index')
        except Exception as e:
            messages.error(request, f'Ошибка при регистрации: {str(e)}')
            return render(request, 'auth/reg.html')

    return render(request, 'auth/reg.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('login')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user)
            messages.success(request, 'Вы успешно вошли в систему')
            return redirect('index')
        else:
            messages.error(request, 'Неверное имя пользователя или пароль')
            return render(request, 'auth/login.html')
    
    return render(request, 'auth/login.html')

def logout(request):
    auth_logout(request)
    messages.info(request, 'Вы вышли из системы')
<<<<<<< HEAD
<<<<<<< HEAD
    return redirect('login')

def basket(request):
    if not request.user.is_authenticated:
        return redirect('login')
<<<<<<< HEAD

    address = request.session.get('delivery_address', 'Адрес не указан')
    latitude = request.session.get('delivery_latitude', '')
    longitude = request.session.get('delivery_longitude', '')
=======
    
    request.session['delivery_address'] = "Улица Пушкина, дом 42"
    request.session['delivery_latitude'] = "55.123456"
    request.session['delivery_longitude'] = "37.123456"
    request.session.modified = True
>>>>>>> 7740582 (Commit: +API Geoapify + OpenStreetMaps new 2 html + address)

    user = request.user
    basket_items = Basket.objects.filter(user=user)
    total_price = sum(item.product.price * item.quantity for item in basket_items)

    context = {
        'basket_items': basket_items,
        'total_price': total_price,
        'delivery_address': address,
        'latitude': latitude,
        'longitude': longitude,
    }
    return render(request, 'blog/basket.html', context)


def add_basket(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    if request.method == 'POST':
        product_id = request.POST.get('flower_id')
        user = request.user
        
        try:
            product = Flowers.objects.get(id=product_id)
            
            if product.stock < -1000:
                messages.error(request, 'Этот цветок закончился в наличии')
                return redirect(request.META.get('HTTP_REFERER', 'index'))
            
            basket_item, created = Basket.objects.get_or_create(
                product=product,
                user=user,
                defaults={'quantity': 1}
            )
            
            if not created:
                if basket_item.quantity >= product.stock:
                    messages.error(request, 'Достигнуто максимальное количество для этого цветка')
                    return redirect('basket')
                basket_item.quantity += 1
                basket_item.save()
                
            messages.success(request, 'Товар добавлен в корзину')
        except Flowers.DoesNotExist:
            messages.error(request, 'Товар не найден')
            
    return redirect('basket')

def update_quantity(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        action = request.POST.get('action')

        print("Полученные данные:", {"item_id": item_id, "action": action})

        if not item_id or not action:
            messages.error(request, 'Некорректные данные. Попробуйте ещё раз.')
            return redirect('basket')

        try:
            basket_item = Basket.objects.get(id=item_id, user=request.user)
            product = basket_item.product

            if product.stock < 0:
                print(f"Товар '{product.title}' с id {product.id} имеет отрицательный stock: {product.stock}. Увеличение невозможно.")
                messages.error(request, f'Товар "{product.title}" больше недоступен.')
                return redirect('basket')

            if product.stock == 0 and action == 'increase':
                print(f"Товар '{product.title}' с id {product.id} имеет stock 0. Увеличение невозможно.")
                messages.error(request, f'Товар "{product.title}" закончился на складе.')
                return redirect('basket')

            if action == 'increase':
                print(f"Попытка увеличить товар: {product.title}, текущий stock: {product.stock}, текущее количество: {basket_item.quantity}")
                if basket_item.quantity >= product.stock:
                    messages.error(request, 'Недостаточно товара на складе.')
                else:
                    basket_item.quantity += 1
                    basket_item.save()
                    messages.success(request, f'Количество товара "{product.title}" увеличено до {basket_item.quantity}.')

            elif action == 'decrease':
                print(f"Попытка уменьшить товар: {product.title}, текущее количество: {basket_item.quantity}")
                if basket_item.quantity > 1:
                    basket_item.quantity -= 1
                    basket_item.save()
                    messages.success(request, f'Количество товара "{product.title}" уменьшено до {basket_item.quantity}.')
                else:
                    basket_item.delete()
                    messages.success(request, f'Товар "{product.title}" удалён из корзины.')

            return redirect('basket')

        except Basket.DoesNotExist:
            print(f"Ошибка: Товар с id {item_id} не найден в корзине пользователя {request.user}.")
            messages.error(request, 'Товар не найден в корзине.')
        except Exception as e:
            print(f"Ошибка в update_quantity: {e}")
            messages.error(request, 'Произошла ошибка. Попробуйте ещё раз.')

    return redirect('basket')

def remove_from_basket(request, item_id):
    if not request.user.is_authenticated:
        return redirect('login')
    
    basket_item = get_object_or_404(Basket, id=item_id, user=request.user)
    basket_item.delete()
    
    return redirect('basket')

@login_required
def delivery_view(request):
<<<<<<< HEAD
    address = request.session.get('delivery_address', 'Адрес не указан')
    latitude = request.session.get('delivery_latitude', '')
    longitude = request.session.get('delivery_longitude', '')

    if address == 'Адрес не указан':
        return redirect('basket')

    basket_items = Basket.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in basket_items)

    context = {
        'address': address,
        'latitude': latitude,
        'longitude': longitude,
        'basket_items': basket_items,
        'total_price': total_price,
    }
    return render(request, 'blog/delivery.html', context)
    
def order_success(request, order_id):
    try:
        order = get_object_or_404(Order, id=order_id)
        
        if request.user != order.user:
            raise Http404("Это не ваш заказ")
        
        return render(request, 'blog/order_success.html', {
            'order': order,
            'order_items': order.ordertime_set.all()  
        })
        
    except Exception as e:
        print(f"Ошибка в order_success: {str(e)}")
        raise Http404("Произошла ошибка при отображении заказа")
=======
    if request.method == 'POST':
        # Получаем данные из формы корзины
        address = request.POST.get('address', 'ул. Александра Пушкина, 42')
        latitude = request.POST.get('latitude', '')
        longitude = request.POST.get('longitude', '')
        
        # Собираем товары из корзины
        basket_items = []
        for key, value in request.POST.items():
            if key.startswith('product_'):
                product_id = key.replace('product_', '')
                # Здесь вам нужно получить продукт из базы данных
                # и добавить в basket_items
                
        context = {
            'address': address,
            'latitude': latitude,
            'longitude': longitude,
            'basket_items': basket_items,
            'total_price': request.session.get('total_price', 0)
        }
        return render(request, 'blog/delivery.html', context)
    else:
        # Если зашли напрямую без выбора адреса
        return redirect('basket')  # Перенаправляем обратно в корзин
    
@login_required
def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order_items = OrderTime.objects.filter(order=order)
    
    context = {
        'order': order,
        'order_items': order_items,
    }
    return render(request, 'blog/order_success.html', context)

>>>>>>> 7740582 (Commit: +API Geoapify + OpenStreetMaps new 2 html + address)
    
@login_required
def process_delivery(request):
    if request.method == 'POST':
<<<<<<< HEAD
        try:
            address = request.POST.get('address', '').strip()
            latitude = request.POST.get('latitude', '').strip()
            longitude = request.POST.get('longitude', '').strip()

            if not address:
                print("Ошибка: адрес не передан через POST")
                messages.error(request, 'Адрес доставки не указан.')
                return redirect('delivery') 

            required_fields = {
                'fullname': 'ФИО',
                'email': 'Email',
                'phone': 'Телефон',
                'delivery_time': 'Время доставки'
            }

            errors = []
            for field, name in required_fields.items():
                if not request.POST.get(field):
                    errors.append(f"Поле '{name}' обязательно для заполнения.")
            
            if errors:
                messages.error(request, '\n'.join(errors))
                return redirect('delivery')  

            request.session['delivery_address'] = address
            request.session['delivery_latitude'] = latitude
            request.session['delivery_longitude'] = longitude
            request.session['delivery_data'] = {
                'address': address,
                'latitude': latitude,
                'longitude': longitude,
                'fullname': request.POST['fullname'].strip(),
                'email': request.POST['email'].strip(),
                'phone': request.POST['phone'].strip(),
                'delivery_time': request.POST['delivery_time'].strip(),
                'comment': request.POST.get('comment', '').strip()
            }
            request.session.modified = True
            print("Обновлённая сессия:", request.session['delivery_data'])

            basket_items = Basket.objects.filter(user=request.user)
            if not basket_items.exists():
                messages.error(request, 'Ваша корзина пуста.')
                return redirect('basket')  

            return HttpResponseRedirect(reverse('complete_order'))  

        except Exception as e:
            print(f"Ошибка в process_delivery: {str(e)}")
            messages.error(request, 'Ошибка обработки данных. Попробуйте ещё раз.')
            return redirect('delivery')  

    return redirect('delivery')  

@login_required
def complete_order(request):
    try:
        delivery_data = request.session.get('delivery_data', {})
        if not delivery_data:
            raise ValueError("Нет данных доставки в сессии")

        basket_items = list(Basket.objects.filter(user=request.user))
        if not basket_items:
            raise ValueError("Корзина пуста")

        order_data = {
            'user': request.user,
            'address': delivery_data.get('address', ''),
            'customer_name': delivery_data.get('fullname', ''),
            'phone': delivery_data.get('phone', ''),
            'email': delivery_data.get('email', ''),
            'delivery_time': delivery_data.get('delivery_time', ''),
            'comment': delivery_data.get('comment', ''),
            'total_amount': sum(item.product.price * item.quantity for item in basket_items),
            'status_order': 'processing'
        }

        order = Order.objects.create(**order_data)
=======
        address = request.session.get('delivery_address')
        if not address:
            messages.error(request, 'Адрес доставки не указан')
            return redirect('basket')
        
        try:
            # Проверка обязательных полей
            required_fields = {
                'fullname': 'ФИО',
                'email': 'Email',
                'phone': 'Телефон', 
                'delivery_time': 'Время доставки',
                'address': 'Адрес'
            }
            
            errors = []
            for field, name in required_fields.items():
                if not request.POST.get(field):
                    errors.append(f"Поле '{name}' обязательно для заполнения")
            
            if errors:
                messages.error(request, '\n'.join(errors))
                return redirect('delivery')

            # Сохранение данных в сессии
            request.session['delivery_data'] = {
                'address': request.POST['address'],
                'latitude': request.POST.get('latitude', ''),
                'longitude': request.POST.get('longitude', ''),
                'fullname': request.POST['fullname'],
                'email': request.POST['email'],
                'phone': request.POST['phone'],
                'delivery_time': request.POST['delivery_time'],
                'comment': request.POST.get('comment', '')
            }
            
            # Принудительное сохранение сессии
            request.session.modified = True
            request.session.save()
            
            print("Данные сессии установлены:", request.session['delivery_data'])
            
            # Проверка корзины
            basket_items = Basket.objects.filter(user=request.user)
            if not basket_items.exists():
                messages.error(request, 'Ваша корзина пуста')
                return redirect('basket')
            
            print("Перенаправление на complete_order")
            return HttpResponseRedirect(reverse('complete_order'))
            
        except Exception as e:
            print(f"Ошибка в process_delivery: {str(e)}")
            messages.error(request, 'Ошибка обработки данных')
            return redirect('delivery')
    
    return redirect('delivery')

@login_required
def complete_order(request):
    print("\n=== START complete_order ===")
    print(f"Session ID: {request.session.session_key}")
    print("All session data:", dict(request.session))
    
    # Проверка данных доставки в сессии
    if 'delivery_data' not in request.session:
        error_msg = "ОШИБКА: Нет данных доставки в сессии!"
        print(error_msg)
        messages.error(request, 'Данные доставки не найдены. Пожалуйста, заполните форму еще раз.')
        return redirect('delivery')

    try:
        delivery_data = request.session['delivery_data']
        print("\nDelivery data from session:", delivery_data)
        
        # Получаем товары из корзины
        basket_items = Basket.objects.filter(user=request.user).select_related('product')
        if not basket_items.exists():
            error_msg = "ОШИБКА: Корзина пуста!"
            print(error_msg)
            messages.error(request, 'Ваша корзина пуста')
            return redirect('basket')
        
        print(f"\nBasket items ({basket_items.count()}):")
        for item in basket_items:
            print(f"- {item.product.title} x {item.quantity}")

        # Проверка остатков товаров
        out_of_stock = []
        for item in basket_items:
            if item.quantity > item.product.stock:
                out_of_stock.append({
                    'product': item.product.title,
                    'requested': item.quantity,
                    'available': item.product.stock
                })

        if out_of_stock:
            error_msg = "ОШИБКА: Недостаточно товаров на складе!"
            print(error_msg)
            for item in out_of_stock:
                print(f"- {item['product']}: запрошено {item['requested']}, доступно {item['available']}")
                messages.error(request, 
                    f'Недостаточно товара "{item["product"]}" на складе (доступно: {item["available"]})')
            return redirect('basket')

        # Создание заказа
        total_amount = sum(item.product.price * item.quantity for item in basket_items)
        print(f"\nCreating order with total amount: {total_amount}")
        
        order = Order.objects.create(
            user=request.user,
            address=delivery_data['address'],
            customer_name=delivery_data['fullname'],
            phone=delivery_data['phone'],
            email=delivery_data['email'],
            delivery_time=delivery_data['delivery_time'],
            comment=delivery_data.get('comment', ''),
            total_amount=total_amount,
            status_order='processing'
        )
        print(f"Order created - ID: {order.id}")

        # Создание позиций заказа и обновление остатков
        print("\nCreating order items:")
>>>>>>> 7740582 (Commit: +API Geoapify + OpenStreetMaps new 2 html + address)
        for item in basket_items:
            OrderTime.objects.create(
                order=order,
                flower=item.product,
                quantity=item.quantity,
                unit_price=item.product.price
            )
            item.product.stock -= item.quantity
            item.product.save()
<<<<<<< HEAD

        Basket.objects.filter(user=request.user).delete()
        del request.session['delivery_data']
        request.session.modified = True

        return redirect('order_success', order_id=order.id)

    except Exception as e:
        print("ERROR in complete_order:", str(e))
        messages.error(request, f'Ошибка оформления заказа: {str(e)}')
        return redirect('delivery')
    
def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    categories = Category.objects.all() 
    flowers = Flowers.objects.filter(category=category) 
    return render(request, 'blog/category_detail.html', {
        'category': category,
        'categories': categories,  
        'flowers': flowers
    })

@csrf_exempt
def save_delivery_data(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            request.session['delivery_address'] = data.get('address')
            request.session['delivery_latitude'] = data.get('latitude')
            request.session['delivery_longitude'] = data.get('longitude')
            request.session.modified = True
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request'})
=======
    return render(
        request,
        'blog/index.html',
        context,
    )

>>>>>>> 02e56ac (Commit: Update HTML)
=======
    return render(request, 'blog/flower_detail.html', context)
>>>>>>> 3741d9c (Update HTML + flower_detail + interface)
=======
    return redirect('login_view')
>>>>>>> bf0b456 (Commit: +Login +Reg)
=======
    return redirect('login')
>>>>>>> 8d08e9a (Commit: +Update code index.html and flower_detail.html)
=======
            print(f"- Added {item.product.title} x {item.quantity}")

        # Очистка корзины
        basket_items.delete()
        print("Basket cleared")

        # Очистка сессии
        del request.session['delivery_data']
        request.session.modified = True
        print("Delivery data removed from session")

        print(f"\nRedirecting to order_success with order_id: {order.id}")
        return redirect('order_success', order_id=order.id)

    except KeyError as e:
        error_msg = f"ОШИБКА: Отсутствует обязательное поле в данных доставки - {str(e)}"
        print(error_msg)
        messages.error(request, 'Ошибка в данных доставки. Пожалуйста, заполните форму еще раз.')
        return redirect('delivery')

    except IntegrityError as e:
        error_msg = f"ОШИБКА ЦЕЛОСТНОСТИ ДАННЫХ: {str(e)}"
        print(error_msg)
        messages.error(request, 'Ошибка при создании заказа. Пожалуйста, попробуйте еще раз.')
        return redirect('delivery')

    except Exception as e:
        error_msg = f"НЕОЖИДАННАЯ ОШИБКА: {str(e)}"
        print(error_msg)
        import traceback
        traceback.print_exc()
        messages.error(request, 'Произошла непредвиденная ошибка. Пожалуйста, попробуйте позже.')
        return redirect('delivery')
>>>>>>> 7740582 (Commit: +API Geoapify + OpenStreetMaps new 2 html + address)
