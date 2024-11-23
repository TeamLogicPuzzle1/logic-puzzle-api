# Generated by Django 5.1.3 on 2024-11-20 19:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food_waste', '0002_alter_foodwaste_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='foodwaste',
            name='quantity',
            field=models.IntegerField(choices=[(0, '1L'), (1, '2L'), (2, '3L'), (3, '5L'), (4, '10L'), (5, '20L')], default=0, help_text='0 : 1L, 1 : 2L, 2 : 3L, 3 : 5L, 4 : 10L, 5 : 20L'),
        ),
    ]