# Generated by Django 4.2.1 on 2023-10-09 08:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facility', '0040_alter_facility_mainrules_facility_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facility_mainrules',
            name='facility',
            field=models.CharField(default=None, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='facility_subrules',
            name='facility',
            field=models.CharField(default=None, max_length=100, null=True),
        ),
    ]
