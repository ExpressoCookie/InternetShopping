# Generated by Django 3.2.9 on 2021-12-15 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_rename_item_name_item_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='nutrient',
            field=models.CharField(max_length=100),
        ),
    ]
