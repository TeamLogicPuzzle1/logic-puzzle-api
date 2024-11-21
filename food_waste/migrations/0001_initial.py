# Generated by Django 5.0.7 on 2024-11-14 14:48

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FoodWaste',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.FloatField(choices=[(1, '1L'), (3, '3L'), (5, '5L'), (10, '10L'), (20, '20L')])),
                ('date_recorded', models.DateField(auto_now_add=True)),
                ('date', models.DateField(db_index=True, default=datetime.date.today)),
                ('user', models.ForeignKey(default='', max_length=20, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'food_waste',
                'ordering': ['-date'],
            },
        ),
    ]
