# Generated by Django 2.0.6 on 2018-07-28 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cm', '0022_party_gender'),
    ]

    operations = [
        migrations.AddField(
            model_name='party',
            name='caste',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
