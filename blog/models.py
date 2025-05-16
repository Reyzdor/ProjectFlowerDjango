from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from django.utils.text import slugify  

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
    image_two = models.ImageField(
        verbose_name='вторая картинка',
        upload_to='uploads/',
    )

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
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='заказ')
    flower = models.ForeignKey(Flowers, on_delete=models.CASCADE, verbose_name='цветок')
    
    quantity = models.PositiveIntegerField(
        verbose_name='количество',
    )

    unit_price = models.DecimalField(
        verbose_name='цена за единицу',
        max_digits=10,
        decimal_places=2,
        editable=False,  # нельзя редактировать
    )

    def get_total(self):
        # Проверяем, что оба значения установлены
        if self.unit_price is None or self.quantity is None:
            return 0  # Если одно из значений None, возвращаем 0
        return self.unit_price * self.quantity

    def save(self, *args, **kwargs):
        # Если цена не была установлена, берём из модели цветка
        if not self.unit_price:
            self.unit_price = self.flower.price  # фиксируем цену при создании
        super().save(*args, **kwargs)

        # Пересчитываем общую сумму в заказе
        self.order.total_amount = sum(
            item.get_total() for item in self.order.ordertime_set.all()
        )
        self.order.save()

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
    quantity = models.PositiveIntegerField(
        default=1,
        verbose_name='количество'
    )
    created_timestamp = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return f"Корзина для {self.user} | Товар {self.product}"

    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'product'], 
                name='unique_user_product'
            ),
        ]


    