# Generated by Django 2.2.6 on 2020-06-21 03:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home_application', '0004_auto_20200619_2339'),
    ]

    operations = [
        migrations.AlterField(
            model_name='business',
            name='bk_biz_id',
            field=models.IntegerField(verbose_name='业务ID'),
        ),
    ]