# Generated by Django 4.1.3 on 2022-11-22 22:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0004_company_date_joined'),
    ]

    operations = [
        migrations.AlterField(
            model_name='storeimages',
            name='company',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='pictures', to='company.company'),
        ),
    ]
