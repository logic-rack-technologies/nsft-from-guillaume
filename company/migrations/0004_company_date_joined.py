# Generated by Django 4.1.3 on 2022-11-22 21:49

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0003_alter_storeimages_options_alter_storeimages_company'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='date_joined',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
