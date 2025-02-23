# Generated by Django 4.0.2 on 2022-02-11 01:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Home',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True)),
                ('rent_date', models.IntegerField(null=True)),
                ('rent_month', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Utility',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=10, null=True)),
                ('month', models.IntegerField(blank=True, null=True)),
                ('date', models.IntegerField(blank=True, null=True)),
                ('home', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='utility', to='setting.home')),
            ],
        ),
        migrations.CreateModel(
            name='LiveIn',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField(auto_now=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('home', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='setting.home')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Invite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_accepted', models.BooleanField(default=False)),
                ('invited_at', models.DateTimeField(auto_now=True)),
                ('home', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='setting.home')),
                ('receive_user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
