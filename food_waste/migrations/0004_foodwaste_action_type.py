# Generated by Django 5.0.7 on 2024-11-21 02:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food_waste', '0003_alter_foodwaste_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='foodwaste',
            name='action_type',
            field=models.IntegerField(choices=[(0, '+'), (1, '-')], default=0, help_text='Action type: 0 for addition (+), 1 for reduction (-)'),
        ),
    ]
