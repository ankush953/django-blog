# Generated by Django 2.1.7 on 2019-04-13 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_auto_20190412_1828'),
    ]

    operations = [
        migrations.AlterField(
            model_name='siteuser',
            name='bio',
            field=models.TextField(blank=True, max_length=200),
        ),
    ]
