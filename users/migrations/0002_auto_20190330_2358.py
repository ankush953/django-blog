# Generated by Django 2.1.7 on 2019-03-30 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='siteuser',
            name='profile_pic',
            field=models.ImageField(blank=True, default='profile_pic/default-user.jpg', upload_to='profile_pic/'),
        ),
    ]