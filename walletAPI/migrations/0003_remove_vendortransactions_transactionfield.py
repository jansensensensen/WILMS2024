# Generated by Django 4.2.5 on 2023-10-10 15:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('walletAPI', '0002_vendortransactions_transactionfield'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vendortransactions',
            name='transactionfield',
        ),
    ]
