# Generated by Django 4.2.1 on 2023-11-07 07:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('facility', '0070_transaction'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facility_mainrules',
            name='facility',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='facility.facility'),
        ),
    ]
