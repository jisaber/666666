# Generated by Django 2.0.4 on 2018-04-30 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20180430_1510'),
    ]

    operations = [
        migrations.CreateModel(
            name='Infect_source',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('infect_id', models.CharField(max_length=10)),
                ('timestamp', models.DateTimeField(null=True)),
            ],
        ),
    ]
