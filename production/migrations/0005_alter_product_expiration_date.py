# Generated by Django 5.0.7 on 2024-09-17 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('production', '0004_remove_product_created_at_remove_product_ocr_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='expiration_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
