# Generated by Django 2.1.7 on 2019-04-22 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_auto_20190414_0032'),
    ]

    operations = [
        migrations.AlterField(
            model_name='siteuser',
            name='bio',
            field=models.TextField(blank=True, max_length=400),
        ),
    ]
