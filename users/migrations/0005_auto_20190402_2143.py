# Generated by Django 2.1.7 on 2019-04-02 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20190402_2142'),
    ]

    operations = [
        migrations.AlterField(
            model_name='siteuser',
            name='firstname',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='siteuser',
            name='lastname',
            field=models.CharField(max_length=20),
        ),
    ]
