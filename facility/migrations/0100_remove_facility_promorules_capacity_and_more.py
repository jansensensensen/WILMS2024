# Generated by Django 4.2.5 on 2023-12-17 11:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facility', '0099_facility_promorules_num_attendies_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='facility_promorules',
            name='capacity',
        ),
        migrations.RemoveField(
            model_name='facility_promorules_set',
            name='capacity',
        ),
    ]
