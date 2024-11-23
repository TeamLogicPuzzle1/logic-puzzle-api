# Generated by Django 5.0.7 on 2024-11-19 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('production', '0004_alter_product_category_alter_product_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.IntegerField(choices=[(0, '미분류'), (1, '고기'), (2, '해산물'), (3, '유제품'), (4, '야채'), (5, '음료'), (6, '과일'), (7, '기타')], default=0, help_text='0 : 미분류, 1 : 고기, 2 : 해산물, 3 : 유제품, 4 : 야채, 5 : 음료, 6 : 과일, 7 : 기타'),
        ),
        migrations.AlterField(
            model_name='product',
            name='location',
            field=models.IntegerField(choices=[(0, '냉장'), (1, '냉동'), (2, '상온'), (3, '미분류')], default=0, help_text='0 : 냉장, 1 : 냉동, 2 : 상온, 3 : 미분류'),
        ),
    ]
