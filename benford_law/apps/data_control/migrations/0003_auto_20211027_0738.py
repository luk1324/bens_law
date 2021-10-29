# Generated by Django 3.2.8 on 2021-10-27 07:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('data_control', '0002_auto_20211026_1234'),
    ]

    operations = [
        migrations.RenameField(
            model_name='columnnames',
            old_name='dataset_id',
            new_name='dataset',
        ),
        migrations.RenameField(
            model_name='datavalues',
            old_name='dataset_id',
            new_name='dataset',
        ),
        migrations.RenameField(
            model_name='setscore',
            old_name='dataset_id',
            new_name='dataset',
        ),
        migrations.CreateModel(
            name='BenfordDistributions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
                ('occurence', models.FloatField()),
                ('dataset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data_control.datasets')),
            ],
        ),
    ]
