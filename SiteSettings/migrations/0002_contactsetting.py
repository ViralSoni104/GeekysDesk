# Generated by Django 3.1.5 on 2021-01-20 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SiteSettings', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactSetting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Contact_Type', models.CharField(max_length=50)),
                ('Contact', models.CharField(max_length=255)),
            ],
        ),
    ]
