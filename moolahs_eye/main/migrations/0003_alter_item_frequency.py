# Generated by Django 4.1.5 on 2023-02-05 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_item'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='frequency',
            field=models.IntegerField(choices=[(1, 'daily'), (7, 'weekly'), (30, 'monthly')], default=7),
        ),
    ]
