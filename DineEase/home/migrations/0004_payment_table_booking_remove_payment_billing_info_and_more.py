# Generated by Django 4.2.4 on 2023-10-24 08:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_remove_tablebooking_menu_tablebooking_selected_items_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='table_booking',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='home.tablebooking'),
        ),
        migrations.RemoveField(
            model_name='payment',
            name='billing_info',
        ),
        migrations.AddField(
            model_name='payment',
            name='billing_info',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='home.billinginformation'),
        ),
    ]
