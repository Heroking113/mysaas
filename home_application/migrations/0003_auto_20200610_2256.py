# Generated by Django 2.2.6 on 2020-06-10 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home_application', '0002_auto_20200610_2247'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hostinfo',
            name='bk_cpu',
            field=models.IntegerField(blank=True, null=True, verbose_name='核数'),
        ),
    ]
