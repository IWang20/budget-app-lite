# Generated by Django 4.2.17 on 2025-01-30 02:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upload_pdf', '0002_remove_months_month_remove_months_year'),
    ]

    operations = [
        migrations.AddField(
            model_name='months',
            name='year',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
