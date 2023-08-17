# Generated by Django 4.2.4 on 2023-08-12 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bills', '0004_alter_bill_amount_alter_payment_amount_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=7),
        ),
        migrations.AlterField(
            model_name='payment',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=7),
        ),
        migrations.AlterField(
            model_name='payment',
            name='amount_to_pay',
            field=models.DecimalField(decimal_places=2, max_digits=7),
        ),
        migrations.AlterField(
            model_name='room',
            name='area',
            field=models.DecimalField(decimal_places=2, max_digits=7),
        ),
    ]