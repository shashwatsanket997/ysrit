# Generated by Django 2.0.6 on 2018-07-15 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cm', '0018_telguefile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='telguefile',
            name='tf',
            field=models.FileField(null=True, upload_to='import/'),
        ),
    ]
