# Generated by Django 5.1.1 on 2024-10-07 10:05

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_alter_customuser_profile_picture'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customuser',
            options={'ordering': ['username', '-date_joined'], 'verbose_name': 'User', 'verbose_name_plural': 'Users'},
        ),
        migrations.CreateModel(
            name='Subscribe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('user_from', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Subscribe_from', to=settings.AUTH_USER_MODEL)),
                ('user_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Subscribe_to', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Subscribe',
                'verbose_name_plural': 'Subscribes',
                'ordering': ['-date'],
            },
        ),
    ]
