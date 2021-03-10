# Generated by Django 3.1.5 on 2021-02-25 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GeekysDesk', '0032_auto_20210222_1725'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contact_name', models.CharField(max_length=50)),
                ('contact_email', models.EmailField(max_length=255)),
                ('contact_subject', models.CharField(max_length=255)),
                ('message', models.TextField()),
                ('contacted_on', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='post',
            name='status',
            field=models.CharField(choices=[('True', 'True'), ('False', 'False')], default=True, max_length=10),
        ),
    ]