# Generated by Django 4.1.6 on 2023-03-15 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0011_remove_companymodel_images_remove_usermodel_images_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companymodel',
            name='image',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='usermodel',
            name='image',
            field=models.TextField(blank=True),
        ),
    ]
