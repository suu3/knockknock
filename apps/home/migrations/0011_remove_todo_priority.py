# Generated by Django 4.0.1 on 2022-02-20 08:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0010_alter_livingrule_cate'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='todo',
            name='priority',
        ),
    ]
