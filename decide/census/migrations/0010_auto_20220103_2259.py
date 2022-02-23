# Generated by Django 2.0 on 2022-01-03 22:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('census', '0009_auto_20211228_1907'),
    ]

    operations = [
        migrations.AlterField(
            model_name='census',
            name='voter_ids',
            field=models.ManyToManyField(to='census.Voter'),
        ),
        migrations.AlterField(
            model_name='voter',
            name='edad',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='voter',
            name='genero',
            field=models.TextField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='voter',
            name='location',
            field=models.TextField(blank=True, max_length=50, null=True),
        ),
    ]