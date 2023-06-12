# Generated by Django 4.1.7 on 2023-03-18 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_id', models.IntegerField()),
                ('title', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=250)),
                ('starting_bid', models.FloatField(max_length=100)),
                ('url', models.URLField()),
                ('category', models.CharField(max_length=50)),
            ],
        ),
    ]
