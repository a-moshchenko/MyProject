# Generated by Django 3.1 on 2020-08-11 21:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='avatar',
            field=models.ImageField(default='not_available.jpg', upload_to='user_photo', verbose_name='Фото'),
        ),
    ]
