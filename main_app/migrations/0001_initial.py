# Generated by Django 3.2 on 2021-05-08 23:24

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
            name='Budget',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('initial_funds', models.IntegerField()),
                ('trip_destination', models.CharField(max_length=60)),
                ('trip_description', models.TextField(max_length=255)),
                ('remaining_funds', models.IntegerField(null=True)),
                ('total_spent', models.IntegerField(null=True)),
                ('color', models.CharField(max_length=100, null=True)),
                ('city', models.CharField(max_length=25, null=True)),
                ('theme', models.CharField(choices=[('Baby Kittens', 'Baby Kittens'), ('Golden Retriever Puppies', 'Golden Retriever Puppies'), ('None', 'None')], default='Baby Kittens', max_length=25, null=True)),
                ('percentage_difference', models.CharField(max_length=10, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='PurchasePhotos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=200)),
                ('budget', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.budget')),
            ],
        ),
        migrations.CreateModel(
            name='Expenditure',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
                ('description', models.TextField(max_length=255)),
                ('amount', models.FloatField()),
                ('date', models.DateField(verbose_name='Purchase date')),
                ('budget', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.budget')),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
