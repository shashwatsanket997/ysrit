# Generated by Django 2.0.6 on 2018-08-28 04:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cm', '0029_auto_20180827_1847'),
    ]

    operations = [
        migrations.AlterField(
            model_name='party',
            name='gram_panchayat',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cm.GramPanchayat'),
        ),
        migrations.AlterField(
            model_name='party',
            name='village',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cm.Village'),
        ),
    ]
