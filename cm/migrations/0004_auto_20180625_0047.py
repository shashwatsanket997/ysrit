# Generated by Django 2.0.6 on 2018-06-24 19:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cm', '0003_auto_20180624_2307'),
    ]

    operations = [
        migrations.CreateModel(
            name='GramPanchayat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gram_panchayat', models.CharField(blank=True, max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Mandal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mandal', models.CharField(blank=True, max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Village',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('village', models.CharField(blank=True, max_length=500)),
                ('gram_panchayat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cm.GramPanchayat')),
            ],
        ),
        migrations.AddField(
            model_name='grampanchayat',
            name='mandal',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cm.Mandal'),
        ),
    ]
