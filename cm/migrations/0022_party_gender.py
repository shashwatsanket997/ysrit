# Generated by Django 2.0.6 on 2018-07-23 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cm', '0021_auto_20180720_1609'),
    ]

    operations = [
        migrations.AddField(
            model_name='party',
            name='gender',
            field=models.CharField(choices=[('Male', 'MALE'), ('Female', 'FEMALE')], default='', max_length=6, null=True),
        ),
    ]
