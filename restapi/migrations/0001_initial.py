# Generated by Django 2.2.1 on 2019-05-31 19:47

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
            name='Stock',
            fields=[
                ('name', models.CharField(max_length=200)),
                ('ticker', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('price', models.FloatField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Invest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.TimeField()),
                ('share', models.FloatField(max_length=100)),
                ('ticker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restapi.Stock')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
