# Generated by Django 3.2 on 2021-05-02 02:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_purchasephotos'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='purchasephotos',
            name='description',
        ),
    ]