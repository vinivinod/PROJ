# Generated by Django 4.2.4 on 2023-09-18 03:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0026_alter_menus_submenu'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menus',
            name='sub_submenu',
            field=models.CharField(blank=True, choices=[('Vegetarian', 'Vegetarian'), ('Non-Vegetarian', 'Non-Vegetarian'), ('Water-based', 'Water-based'), ('Milk-based', 'Milk-based')], default='', max_length=50),
        ),
    ]
