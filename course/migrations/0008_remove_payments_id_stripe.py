# Generated by Django 4.2.3 on 2023-08-29 19:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0007_payments_id_stripe'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payments',
            name='id_stripe',
        ),
    ]
