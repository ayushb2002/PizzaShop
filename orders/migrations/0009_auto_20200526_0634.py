# Generated by Django 2.0.3 on 2020-05-26 06:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0008_auto_20200525_0943'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='cost',
            field=models.DecimalField(decimal_places=2, max_digits=6, null=True),
        ),
        migrations.AddField(
            model_name='orders',
            name='size',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
