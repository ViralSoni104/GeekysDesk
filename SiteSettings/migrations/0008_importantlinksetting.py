# Generated by Django 3.1.5 on 2021-02-08 19:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SiteSettings', '0007_delete_importantlinksetting'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImportantLinkSetting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Page_Name', models.CharField(max_length=255)),
                ('Page_Url', models.CharField(choices=[(0, 'home'), (1, 'subscribe-to-newsletter'), (2, 'subscription-confirmation'), (3, 'unsubscribe'), (4, 'logout'), (5, 'login')], max_length=255)),
            ],
        ),
    ]
