# Generated by Django 4.2.1 on 2023-10-24 21:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facility', '0064_alter_revenue_transaction_facility_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='revenue_transaction',
            old_name='charge_payment',
            new_name='add_payment',
        ),
    ]
