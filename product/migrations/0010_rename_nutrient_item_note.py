# Generated by Django 3.2.9 on 2021-12-15 12:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0009_item_gram'),
    ]

    operations = [
        migrations.RenameField(
            model_name='item',
            old_name='nutrient',
            new_name='note',
        ),
    ]