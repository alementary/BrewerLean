# Generated by Django 4.0.3 on 2023-01-31 13:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ebs', '0011_product_product_active'),
        ('product', '0002_alter_productserviceinfo_product'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductOperationsInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('default_package_yield', models.DecimalField(decimal_places=1, default=80.0, max_digits=3)),
                ('product', models.ForeignKey(blank=True, limit_choices_to={'ownership_id': 1}, null=True, on_delete=django.db.models.deletion.SET_NULL, to='ebs.product', verbose_name='Operations Infos')),
            ],
        ),
    ]
