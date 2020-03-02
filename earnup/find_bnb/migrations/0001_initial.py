# Generated by Django 3.0.3 on 2020-03-01 19:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BnBListing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('import_id', models.PositiveIntegerField(blank=True, null=True)),
                ('name', models.TextField(blank=True, null=True)),
                ('host_id', models.PositiveIntegerField(blank=True, null=True)),
                ('host_name', models.TextField(blank=True, null=True)),
                ('neighborhood_group', models.TextField(blank=True, null=True)),
                ('neighborhood', models.TextField(blank=True, null=True)),
                ('latitude', models.FloatField()),
                ('latitude_radians', models.FloatField()),
                ('longitude', models.FloatField()),
                ('longitude_radians', models.FloatField()),
                ('room_type', models.TextField(blank=True, null=True)),
                ('price', models.PositiveIntegerField(blank=True, null=True)),
                ('minimum_nights', models.PositiveIntegerField(blank=True, null=True)),
                ('number_of_reviews', models.PositiveIntegerField(blank=True, null=True)),
                ('last_review', models.DateField(blank=True, null=True)),
                ('reviews_per_month', models.FloatField(blank=True, null=True)),
                ('calculated_host_listings_count', models.PositiveIntegerField(blank=True, null=True)),
                ('availability_365', models.PositiveIntegerField(blank=True, null=True)),
            ],
        ),
        migrations.AddIndex(
            model_name='bnblisting',
            index=models.Index(fields=['latitude_radians', 'longitude_radians'], name='find_bnb_bn_latitud_4867d9_idx'),
        ),
        migrations.AddIndex(
            model_name='bnblisting',
            index=models.Index(fields=['name', 'neighborhood', 'neighborhood_group', 'room_type'], name='find_bnb_bn_name_818e92_idx'),
        ),
    ]
