# Generated by Django 5.1.7 on 2025-03-27 12:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_flowers_image_two'),
    ]

    operations = [
        migrations.CreateModel(
            name='Basket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stock_basket', models.PositiveIntegerField(default=0)),
                ('created_timestamp', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.flowers')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.user')),
            ],
            options={
                'verbose_name': 'корзина',
            },
        ),
    ]
