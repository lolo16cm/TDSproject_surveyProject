# Generated by Django 5.1.3 on 2024-11-29 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='responses',
            name='responder_email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
    ]