# Generated by Django 2.0.6 on 2018-06-27 09:44

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cm', '0009_partyfilter'),
    ]

    operations = [
        migrations.AlterField(
            model_name='party',
            name='booth_number',
            field=models.CharField(default='', max_length=10),
        ),
        migrations.AlterField(
            model_name='party',
            name='dob',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='party',
            name='father_name',
            field=models.CharField(default='', max_length=500),
        ),
        migrations.AlterField(
            model_name='party',
            name='phone_number',
            field=models.CharField(default='', max_length=13, validators=[django.core.validators.RegexValidator(message='Phone number should be up to 10 digits allowed or you can also write +91.', regex='^\\+?91?\\d{10}$')]),
        ),
        migrations.AlterField(
            model_name='partyfilter',
            name='gram_panchayat',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cm.GramPanchayat'),
        ),
        migrations.AlterField(
            model_name='partyfilter',
            name='mandal',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cm.Mandal'),
        ),
        migrations.AlterField(
            model_name='partyfilter',
            name='party_position',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cm.PartyPosition'),
        ),
        migrations.AlterField(
            model_name='partyfilter',
            name='village',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cm.Village'),
        ),
    ]
