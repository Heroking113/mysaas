# Generated by Django 2.2.6 on 2020-06-28 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home_application', '0009_auto_20200628_2205'),
    ]

    operations = [
        migrations.CreateModel(
            name='QueryParams',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bk_biz_id', models.CharField(max_length=16, verbose_name='业务ID')),
                ('job_instance_id', models.IntegerField(verbose_name='任务实例ID')),
                ('record_id', models.IntegerField(verbose_name='记录的ID')),
            ],
            options={
                'verbose_name': '查询任务的参数',
                'verbose_name_plural': '查询任务的参数',
                'db_table': 'query_param',
            },
        ),
    ]
