# Generated by Django 4.0.2 on 2022-02-18 00:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_alter_todo_cate'),
    ]

    operations = [
        migrations.AddField(
            model_name='todo',
            name='is_not_done_today',
            field=models.BooleanField(default=False),
        ),
    ]
