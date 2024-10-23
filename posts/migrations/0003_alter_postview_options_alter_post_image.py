# Generated by Django 5.1.1 on 2024-10-22 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_postview'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='postview',
            options={'ordering': ['-date'], 'verbose_name': 'PostView', 'verbose_name_plural': 'PostViews'},
        ),
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='prost_pictures/'),
        ),
    ]