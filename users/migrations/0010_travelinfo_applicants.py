# Generated by Django 4.1.4 on 2022-12-24 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_alter_assetrequest_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='travelinfo',
            name='applicants',
            field=models.ManyToManyField(to='users.assetrequest'),
        ),
    ]