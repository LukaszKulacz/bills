# Generated by Django 4.2.4 on 2023-08-08 20:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bills', '0002_alter_bill_description_alter_payment_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='bill',
            name='payments_created',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='bill',
            name='bill_type',
            field=models.CharField(choices=[('RENT', 'Czynsz'), ('HOUSING', 'Spółdzielnia'), ('ELECTRIC', 'Prąd'), ('GAS', 'Gaz'), ('OTHER', 'Inne')], default='HOUSING', max_length=50),
        ),
    ]