# Generated by Django 5.0.4 on 2024-04-21 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryMaster',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('clubbed_name', models.CharField(max_length=100)),
                ('category', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='InsurerMaster',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('insurer', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=100)),
                ('clubbed_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='LOBMaster',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lob', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='MonthMaster',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month', models.CharField(max_length=100)),
                ('month_num', models.IntegerField()),
            ],
        ),
    ]
