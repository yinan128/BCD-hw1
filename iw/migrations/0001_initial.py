# Generated by Django 3.2.7 on 2022-02-04 01:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Facility',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=20)),
                ('name', models.CharField(max_length=50)),
                ('picture', models.FileField(blank=True, upload_to='')),
                ('content_type', models.CharField(max_length=20)),
                ('manufacturer', models.CharField(max_length=20)),
                ('dateInstalled', models.DateField()),
                ('description', models.CharField(max_length=400)),
            ],
        ),
        migrations.CreateModel(
            name='AdditionalPicture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.FileField(blank=True, upload_to='')),
                ('content_type', models.CharField(max_length=20)),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='iw.facility')),
            ],
        ),
    ]
