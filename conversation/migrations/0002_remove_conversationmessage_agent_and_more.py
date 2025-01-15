# Generated by Django 4.2.17 on 2025-01-14 12:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0002_agent_alter_review_options_and_more'),
        ('contenttypes', '0002_remove_content_type_name'),
        ('listings', '0001_initial'),
        ('conversation', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='conversationmessage',
            name='agent',
        ),
        migrations.AddField(
            model_name='conversation',
            name='booking',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='conversations', to='services.booking'),
        ),
        migrations.AddField(
            model_name='conversationmessage',
            name='receiver_id',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='conversationmessage',
            name='receiver_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='receiver_type', to='contenttypes.contenttype'),
        ),
        migrations.AddField(
            model_name='conversationmessage',
            name='sender_id',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='conversationmessage',
            name='sender_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype'),
        ),
        migrations.AlterField(
            model_name='conversation',
            name='listing',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='conversations', to='listings.listing'),
        ),
    ]
