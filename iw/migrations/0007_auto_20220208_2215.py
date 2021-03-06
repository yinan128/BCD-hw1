# Generated by Django 3.2.7 on 2022-02-08 22:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('iw', '0006_merge_0005_auto_20220206_0023_0005_historicdata_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='MainSys',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='SubSys',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('mainSys', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='iw.mainsys')),
            ],
        ),
        migrations.AddField(
            model_name='facility',
            name='subSys',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='iw.subsys'),
        ),
        migrations.AddField(
            model_name='systemdiagram',
            name='subSys',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='iw.subsys'),
        ),
    ]
