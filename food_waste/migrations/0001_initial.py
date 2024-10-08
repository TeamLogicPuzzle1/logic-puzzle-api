from django.db import migrations, models

class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FoodWaste',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(choices=[(1, '1L'), (3, '3L'), (5, '5L'), (10, '10L'), (20, '20L')])),
                ('date', models.DateField(db_index=True)),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
    ]