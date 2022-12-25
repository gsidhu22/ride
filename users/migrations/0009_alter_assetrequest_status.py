# Generated by Django 4.1.4 on 2022-12-24 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_alter_assetrequest_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assetrequest',
            name='status',
            field=models.CharField(choices=[('pending', 'PENDING'), ('expired', 'EXPIRED')], default='pending', max_length=15),
        ),
    ]