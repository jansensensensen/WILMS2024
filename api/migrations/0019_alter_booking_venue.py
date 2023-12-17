# Generated by Django 4.2.6 on 2023-11-29 13:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('facility', '0094_usertype_mainrules_rate_usertype_mainrules_set_rate'),
        ('api', '0018_remove_booking_userid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='venue',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='venue', to='facility.facility'),
        ),
    ]
