# Generated by Django 3.2.9 on 2021-12-07 20:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ebs', '0005_auto_20211015_1436'),
    ]

    operations = [
        migrations.AlterField(
            model_name='batchrawmaterialslog',
            name='is_dh',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='Is Dry Hop?'),
        ),
        migrations.AlterField(
            model_name='schedulepattern',
            name='offset_yeast_harvest',
            field=models.IntegerField(null=True, verbose_name='Days Offset for Yeast Harvest'),
        ),
    ]
