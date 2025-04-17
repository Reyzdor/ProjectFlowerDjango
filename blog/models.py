from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

<<<<<<< HEAD
from django.utils.text import slugify  # Импорт slugify для автоматической генерации slug
=======
>>>>>>> 7740582 (Commit: +API Geoapify + OpenStreetMaps new 2 html + address)

class Category(models.Model):
    title = models.CharField(
        verbose_name='название',
        max_length=255,
    )
    description = models.TextField(
        verbose_name='описание',
        max_length=500,
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='URL-адрес',
        max_length=255,
        blank=True,  
        null=True,   
    )
    
    def save(self, *args, **kwargs):
        if not self.slug:  
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'


class Flowers(models.Model):
    title = models.CharField(
        verbose_name='название',
        max_length=255,
    )
    description = models.TextField(
        verbose_name='описание',
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )
    stock = models.IntegerField(
        default=0,
        verbose_name='количество в наличии',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name='категория',
    )
    date_add = models.DateTimeField(
        auto_now_add=True,
        verbose_name='дата добавления',
    )
    image = models.ImageField(
        verbose_name='картинки',
        upload_to='uploads/',
    )
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> 3741d9c (Update HTML + flower_detail + interface)
    image_two = models.ImageField(
        verbose_name='вторая картинка',
        upload_to='uploads/',
    )
<<<<<<< HEAD
=======
>>>>>>> ad7377b (Update HTML + images + interface)
=======
>>>>>>> 3741d9c (Update HTML + flower_detail + interface)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'цветок'
        verbose_name_plural = 'цветы'


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    address = models.CharField(max_length=255)
    customer_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    delivery_time = models.CharField(max_length=50)
    status_order = models.CharField(max_length=20, default='processing')
    comment = models.TextField(blank=True, null=True, verbose_name='Комментарий к заказу')

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
    
    def __str__(self):
        return f"Заказ #{self.id} - {self.customer_name}"

class OrderTime(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        verbose_name='заказ',
    )
    flower = models.ForeignKey(
        Flowers,
        on_delete=models.CASCADE,
        verbose_name='цветок',
    )
    quantity = models.DecimalField(
        verbose_name='количество',
        max_digits=10,  
        decimal_places=2,  
    )
    unit_price = models.DecimalField(
        verbose_name='цена за единицу',
        max_digits=10,
        decimal_places=2,
    )

    def get_total(self):
        return self.unit_price * self.quantity

    def __str__(self):
        return f"{self.flower.title} - {self.quantity} шт."
    
    class Meta:
        verbose_name = 'позиция'
        verbose_name_plural = 'позиции'


class Basket(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Flowers,
        on_delete=models.CASCADE,   
    )
<<<<<<< HEAD
<<<<<<< HEAD
    quantity = models.PositiveIntegerField(
        default=1,
        verbose_name='количество'
=======
    stock_basket = models.PositiveIntegerField(
        default=0,
>>>>>>> 3741d9c (Update HTML + flower_detail + interface)
=======
    quantity = models.PositiveIntegerField(
        default=1,
        verbose_name='количество'
>>>>>>> bf0b456 (Commit: +Login +Reg)
    )
    created_timestamp = models.DateTimeField(
        auto_now_add=True,
    )
<<<<<<< HEAD
=======

    def __str__(self):
        return f"Корзина для {self.user} | Товар {self.product}"

    
    class Meta:
        verbose_name = 'корзина'

>>>>>>> 3741d9c (Update HTML + flower_detail + interface)

    def __str__(self):
        return f"Корзина для {self.user} | Товар {self.product}"

    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'product'], 
                name='unique_user_product'
            ),
        ]


    