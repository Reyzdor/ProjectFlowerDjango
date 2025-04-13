import json
from django.db import IntegrityError
from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.urls import reverse
from blog.models import Category, Flowers, Basket, Order, OrderTime
from django.contrib.auth.decorators import login_required  
from django.views.decorators.csrf import csrf_exempt


def logout_view(request):
    messages.get_messages(request).used = True  
    logout(request)
    return redirect('blog/login.html')

def index(request):
    categories = Category.objects.all()
    flowers = Flowers.objects.all()[:6]  
    context = {
        'categories': categories,
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
    }
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
    return redirect('login')

def basket(request):
    if not request.user.is_authenticated:
        return redirect('login')

    address = request.session.get('delivery_address', 'Адрес не указан')
    latitude = request.session.get('delivery_latitude', '')
    longitude = request.session.get('delivery_longitude', '')

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
    
@login_required
def process_delivery(request):
    if request.method == 'POST':
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
        for item in basket_items:
            OrderTime.objects.create(
                order=order,
                flower=item.product,
                quantity=item.quantity,
                unit_price=item.product.price
            )
            item.product.stock -= item.quantity
            item.product.save()

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