# Generated by Django 4.1.7 on 2023-06-15 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Rankdarbiai', '0004_promocode'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='address',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='phone_number',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]