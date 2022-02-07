# Generated by Django 4.0.2 on 2022-02-06 05:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('login', '0001_initial'),
        ('auth', '0012_alter_user_first_name_max_length'),
        ('setting', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='home',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='setting.home'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
    ]
