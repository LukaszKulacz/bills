# Generated by Django 4.2.4 on 2023-08-15 12:00

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('bills', '0009_alter_bill_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]