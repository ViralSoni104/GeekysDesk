# Generated by Django 3.1.5 on 2021-01-23 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GeekysDesk', '0022_remove_subscriber_token_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscriber',
            name='token_time',
            field=models.TimeField(default='11:01:29'),
            preserve_default=False,
        ),
    ]
