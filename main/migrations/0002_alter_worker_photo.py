# Generated by Django 5.1.1 on 2024-10-22 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='worker',
            name='photo',
            field=models.ImageField(upload_to='workers/'),
        ),
    ]