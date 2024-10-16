# Generated by Django 5.1.1 on 2024-10-14 23:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_sample_sample_label'),
    ]

    operations = [
        migrations.CreateModel(
            name='Titer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sequencing_run', models.CharField(max_length=255)),
                ('wri_mean_depth', models.CharField(max_length=255)),
                ('dmel_mean_depth', models.CharField(max_length=255)),
                ('wri_titer', models.CharField(max_length=255)),
                ('total_reads', models.IntegerField()),
                ('mapped_reads', models.IntegerField()),
                ('duplicate_reads', models.IntegerField()),
                ('wmel_mean_depth', models.IntegerField()),
                ('wwil_mean_depth', models.IntegerField()),
                ('wmel_titer', models.IntegerField()),
                ('wwil_titer', models.IntegerField()),
                ('dsim_mean_depth', models.IntegerField()),
                ('sample_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.sample')),
            ],
        ),
    ]
