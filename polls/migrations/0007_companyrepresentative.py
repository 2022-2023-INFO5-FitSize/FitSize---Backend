# Generated by Django 4.1.5 on 2023-01-31 08:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0006_alter_clothingtype_id_alter_company_id_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyRepresentative',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('login', models.CharField(blank=True, max_length=100)),
                ('password', models.CharField(blank=True, max_length=200)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.company')),
            ],
        ),
    ]
