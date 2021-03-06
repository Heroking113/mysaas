# Generated by Django 2.2.6 on 2020-06-29 08:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Business',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bk_biz_id', models.IntegerField(verbose_name='业务ID')),
                ('bk_biz_name', models.CharField(max_length=128, verbose_name='业务名称')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('last_edit_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
            ],
            options={
                'verbose_name': '业务信息',
                'verbose_name_plural': '业务信息',
                'db_table': 'business',
            },
        ),
        migrations.CreateModel(
            name='Host',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bk_cloud_id', models.CharField(max_length=32, verbose_name='云区域ID')),
                ('bk_biz_id', models.IntegerField(verbose_name='所属业务的ID')),
                ('bk_cpu', models.IntegerField(blank=True, null=True, verbose_name='核数')),
                ('bk_os_name', models.CharField(blank=True, max_length=32, null=True, verbose_name='操作系统名称')),
                ('bk_host_id', models.IntegerField(verbose_name='主机ID')),
                ('bk_host_innerip', models.CharField(max_length=32, verbose_name='内网IP')),
                ('bk_os_bit', models.CharField(max_length=8, verbose_name='位数')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('last_edit_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
            ],
            options={
                'verbose_name': '主机信息',
                'verbose_name_plural': '主机信息',
                'db_table': 'host',
            },
        ),
        migrations.CreateModel(
            name='LoginBkToken',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bk_token', models.CharField(max_length=256, verbose_name='登录用户的bk_token')),
            ],
            options={
                'verbose_name': '登录用户的bk_token',
                'verbose_name_plural': '登录用户的bk_token',
                'db_table': 'login_bk_token',
            },
        ),
        migrations.CreateModel(
            name='Mission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mission_name', models.CharField(max_length=128, verbose_name='任务名称')),
                ('mission_content', models.TextField(verbose_name='任务内容')),
            ],
            options={
                'verbose_name': '任务信息',
                'verbose_name_plural': '任务信息',
                'db_table': 'mission',
            },
        ),
        migrations.CreateModel(
            name='MissionRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('business_name', models.CharField(max_length=128, verbose_name='业务名称')),
                ('mission_name', models.CharField(max_length=128, verbose_name='任务名称')),
                ('machine_num', models.IntegerField(verbose_name='机器数')),
                ('status', models.CharField(choices=[('1', '未执行'), ('2', '正在执行'), ('3', '执行成功'), ('4', '执行失败'), ('5', '跳过'), ('6', '忽略错误'), ('7', '等待用户'), ('8', '手动结束'), ('9', '状态异常'), ('10', '步骤强制终止中'), ('11', '步骤强制终止成功'), ('12', '步骤强制终止失败'), ('13', '提交失败')], default='1', max_length=32, verbose_name='执行状态')),
                ('job_instance_id', models.IntegerField(blank=True, null=True, verbose_name='任务实例ID')),
                ('operator', models.CharField(max_length=32, verbose_name='操作者')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
            ],
            options={
                'verbose_name': '任务记录',
                'verbose_name_plural': '任务记录',
                'db_table': 'mission_record',
            },
        ),
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
