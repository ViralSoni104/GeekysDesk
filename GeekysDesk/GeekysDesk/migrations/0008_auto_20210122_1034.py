# Generated by Django 3.1.5 on 2021-01-22 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GeekysDesk', '0007_auto_20210122_1033'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscriber',
            name='token_time',
            field=models.TimeField(blank=True, default='', null=True),
        ),
    ]
