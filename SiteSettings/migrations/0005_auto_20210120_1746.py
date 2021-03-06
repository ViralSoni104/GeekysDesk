# Generated by Django 3.1.5 on 2021-01-20 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SiteSettings', '0004_auto_20210120_1743'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactsetting',
            name='Contact_Type',
            field=models.CharField(help_text='Like. Email, Phone, Address etc.', max_length=50),
        ),
        migrations.AlterField(
            model_name='socialmediasetting',
            name='Social_Media_Link',
            field=models.CharField(max_length=255),
        ),
    ]
