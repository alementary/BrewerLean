# Generated by Django 3.1.5 on 2021-01-27 21:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ebs', '0010_auto_20210127_2107'),
    ]

    operations = [
        migrations.AlterField(
            model_name='batchplandates',
            name='batch',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='ebs.batch'),
        ),
    ]
