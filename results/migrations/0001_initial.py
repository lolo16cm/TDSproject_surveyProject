# Generated by Django 5.1.3 on 2024-11-26 03:12

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('answers', '0001_initial'),
        ('create_form', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Responses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('response_code', models.CharField(max_length=20)),
                ('responder_ip', models.CharField(max_length=30)),
                ('responder_email', models.EmailField(blank=True, max_length=254)),
                ('responder', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='responder', to=settings.AUTH_USER_MODEL)),
                ('response', models.ManyToManyField(related_name='response', to='answers.answer')),
                ('response_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='response_to', to='create_form.form')),
            ],
        ),
    ]
