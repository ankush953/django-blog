# Generated by Django 2.1.7 on 2019-04-10 14:09

import articles.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0010_post_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='images',
            name='post',
        ),
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, upload_to=articles.models.imagepath),
        ),
        migrations.DeleteModel(
            name='Images',
        ),
    ]
