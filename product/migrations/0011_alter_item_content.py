# Generated by Django 3.2.9 on 2021-12-16 09:06

from django.db import migrations
import markdownx.models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0010_rename_nutrient_item_note'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='content',
            field=markdownx.models.MarkdownxField(),
        ),
    ]