# Generated by Django 4.2.4 on 2023-08-16 23:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bills', '0011_rename_date_bill_date_created_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='paid',
            field=models.BooleanField(default=False),
        ),
    ]
