# Generated by Django 3.2.16 on 2023-01-25 03:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('databaseQueries', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='public_key',
            field=models.CharField(blank=True, max_length=300),
        ),
    ]
