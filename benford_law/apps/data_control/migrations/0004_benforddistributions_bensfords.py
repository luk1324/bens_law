# Generated by Django 3.2.8 on 2021-10-27 21:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_control', '0003_auto_20211027_0738'),
    ]

    operations = [
        migrations.AddField(
            model_name='benforddistributions',
            name='bensfords',
            field=models.FloatField(default=0.5),
            preserve_default=False,
        ),
    ]