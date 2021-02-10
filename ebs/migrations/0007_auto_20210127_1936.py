# Generated by Django 3.1.5 on 2021-01-27 19:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ebs', '0006_auto_20210127_1756'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='batch',
            options={'verbose_name_plural': 'Batches'},
        ),
        migrations.AlterModelOptions(
            name='batchactualdates',
            options={'verbose_name_plural': 'Batch Actual Dates'},
        ),
        migrations.AlterModelOptions(
            name='batchdoentry',
            options={'verbose_name_plural': 'Batch DO Entries'},
        ),
        migrations.AlterModelOptions(
            name='batchfermentationqc',
            options={'verbose_name_plural': 'Batch Fermentation QC Data'},
        ),
        migrations.AlterModelOptions(
            name='batchplandates',
            options={'verbose_name_plural': 'Batch Plan Dates'},
        ),
        migrations.AlterModelOptions(
            name='batchrawmaterialslog',
            options={'verbose_name_plural': 'Batch Raw Materials Logs'},
        ),
        migrations.AlterModelOptions(
            name='batchsize',
            options={'verbose_name_plural': 'Batch Sizes'},
        ),
        migrations.AlterModelOptions(
            name='batchtransfer',
            options={'verbose_name_plural': 'Batch Transfers'},
        ),
        migrations.AlterModelOptions(
            name='batchwortqc',
            options={'verbose_name_plural': 'Batch Wort QC Data'},
        ),
        migrations.AlterModelOptions(
            name='batchyeastpitch',
            options={'verbose_name_plural': 'Batch Yeast Pitches'},
        ),
        migrations.AlterModelOptions(
            name='canningqc',
            options={'verbose_name_plural': 'Canning QC Data'},
        ),
        migrations.AlterModelOptions(
            name='facility',
            options={'verbose_name': 'Facility', 'verbose_name_plural': 'Facilities'},
        ),
        migrations.AlterModelOptions(
            name='material',
            options={'verbose_name_plural': 'Materials'},
        ),
        migrations.AlterModelOptions(
            name='originator',
            options={'verbose_name_plural': 'Originators'},
        ),
        migrations.AlterModelOptions(
            name='packagingrun',
            options={'verbose_name_plural': 'Packaging Runs'},
        ),
        migrations.AlterModelOptions(
            name='partner',
            options={'verbose_name_plural': 'Partners'},
        ),
        migrations.AlterModelOptions(
            name='partnertype',
            options={'verbose_name_plural': 'Partner Types'},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'verbose_name_plural': 'Products'},
        ),
        migrations.AlterModelOptions(
            name='producttype',
            options={'verbose_name_plural': 'Product Types'},
        ),
        migrations.AlterModelOptions(
            name='schedulepattern',
            options={'verbose_name_plural': 'Schedule Patterns'},
        ),
        migrations.AlterModelOptions(
            name='tank',
            options={'verbose_name_plural': 'Tanks'},
        ),
        migrations.AddField(
            model_name='batchactualdates',
            name='last_modified_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='batchactualdates',
            name='last_modified_on',
            field=models.DateField(auto_now=True),
        ),
        migrations.AddField(
            model_name='batchdoentry',
            name='date',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='schedulepattern',
            name='last_modified_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='schedulepattern',
            name='last_modified_on',
            field=models.DateField(auto_now=True),
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=75, null=True)),
                ('role', models.CharField(choices=[('HS', 'Hot Side'), ('CS', 'Cold Side'), ('WS', 'Warehouse')], default='HS', max_length=2)),
                ('last_modified_on', models.DateField(auto_now=True)),
                ('last_modified_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Staff',
            },
        ),
        migrations.AddField(
            model_name='batchdoentry',
            name='staff',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='ebs.staff'),
        ),
        migrations.AddField(
            model_name='batchfermentationqc',
            name='staff',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='ebs.staff'),
        ),
        migrations.AddField(
            model_name='batchtransfer',
            name='staff',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='ebs.staff'),
        ),
        migrations.AddField(
            model_name='batchwortqc',
            name='brewer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='ebs.staff'),
        ),
        migrations.AddField(
            model_name='batchyeastpitch',
            name='staff',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='ebs.staff'),
        ),
        migrations.AddField(
            model_name='canningqc',
            name='staff',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='ebs.staff'),
        ),
        migrations.AddField(
            model_name='packagingrun',
            name='staff',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='ebs.staff'),
        ),
        migrations.AlterField(
            model_name='batch',
            name='brewer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='ebs.staff'),
        ),
    ]