# Generated by Django 4.2.1 on 2023-05-25 03:47

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_alter_booking_computers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='referenceNo',
            field=models.CharField(blank=True, default=uuid.uuid1, max_length=8, unique=True),
        ),
    ]
