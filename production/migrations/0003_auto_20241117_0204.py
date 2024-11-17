from django.db import migrations

def update_location_values(apps, schema_editor):
    # Product 모델 가져오기 (앱 이름과 모델 이름은 실제 이름으로 변경)
    Product = apps.get_model('production', 'Product')

    # 기존 데이터를 업데이트
    for product in Product.objects.all():
        if product.location == '냉장':
            product.location = 1
        elif product.location == '냉동':
            product.location = 2
        elif product.location == '실외':
            product.location = 3
        else:
            product.location = 4
        product.save()

class Migration(migrations.Migration):
    dependencies = [
        ('production', '0002_alter_product_category_alter_product_expiration_date_and_more'),
    ]

    operations = [
        migrations.RunPython(update_location_values),
    ]