# Generated by Django 4.2.4 on 2023-09-20 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0030_addtocart_delete_cart'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='address',
            field=models.TextField(default='No Address'),
        ),
        migrations.AddField(
            model_name='employee',
            name='education',
            field=models.CharField(default='No Education', max_length=100),
        ),
        migrations.AddField(
            model_name='employee',
            name='emergency_contact_number',
            field=models.CharField(default='No Emergency number', max_length=12),
        ),
        migrations.AddField(
            model_name='employee',
            name='emergency_name',
            field=models.CharField(default='No Emergency name', max_length=100),
        ),
        migrations.AddField(
            model_name='employee',
            name='id_proof_number',
            field=models.CharField(default='No id proof', max_length=100),
        ),
        migrations.AddField(
            model_name='employee',
            name='qualification',
            field=models.CharField(default='No Qualification', max_length=100),
        ),
    ]
