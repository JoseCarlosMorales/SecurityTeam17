# Generated by Django 2.0 on 2021-12-19 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('census', '0005_remove_census_voter_ids'),
    ]

    operations = [
        migrations.AddField(
            model_name='census',
            name='votersIds',
            field=models.ManyToManyField(to='census.Voter'),
        ),
    ]
