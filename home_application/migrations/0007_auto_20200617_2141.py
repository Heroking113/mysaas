# Generated by Django 2.2.6 on 2020-06-17 13:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home_application', '0006_auto_20200614_1132'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='BusinessInfo',
            new_name='Business',
        ),
        migrations.RenameModel(
            old_name='HostInfo',
            new_name='Host',
        ),
        migrations.RenameModel(
            old_name='MissionInfo',
            new_name='Mission',
        ),
        migrations.AlterModelTable(
            name='business',
            table='business',
        ),
        migrations.AlterModelTable(
            name='host',
            table='host',
        ),
        migrations.AlterModelTable(
            name='mission',
            table='mission',
        ),
    ]