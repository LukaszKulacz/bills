# Generated by Django 4.2.4 on 2023-08-12 13:59

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('bills', '0005_alter_bill_amount_alter_payment_amount_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='room',
            name='area',
        ),
        migrations.AddField(
            model_name='room',
            name='date_from',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='room',
            name='date_to',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='room',
            name='mail',
            field=models.EmailField(default='', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='room',
            name='phone',
            field=models.CharField(default='', max_length=20),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='bill',
            name='date',
            field=models.DateField(),
        ),
    ]
