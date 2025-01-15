# Generated by Django 4.2.17 on 2025-01-14 20:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0002_agent_alter_review_options_and_more'),
        ('listings', '0002_alter_listing_options_alter_subimage_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='agent',
            field=models.ForeignKey(limit_choices_to={'is_agent': True}, on_delete=django.db.models.deletion.CASCADE, related_name='listings', to='services.agent'),
        ),
    ]