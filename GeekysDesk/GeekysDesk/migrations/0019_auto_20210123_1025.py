# Generated by Django 3.1.5 on 2021-01-23 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GeekysDesk', '0018_subscriber_token_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscriber',
            name='token_time',
            field=models.TimeField(),
        ),
    ]
