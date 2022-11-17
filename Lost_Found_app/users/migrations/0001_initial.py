# Generated by Django 3.2.16 on 2022-11-17 12:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import djongo.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.URLField(max_length=250)),
                ('image', models.ImageField(blank=True, upload_to='IMGS/')),
                ('content', models.TextField(max_length=5000)),
            ],
        ),
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('chat_id', djongo.models.fields.ObjectIdField(auto_created=True, primary_key=True, serialize=False)),
                ('register_date', models.DateTimeField()),
                ('close_data', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(blank=True, max_length=30)),
                ('phone', models.CharField(blank=True, max_length=20)),
                ('location', models.CharField(blank=True, max_length=10)),
                ('credit_details', models.CharField(blank=True, max_length=16)),
                ('rating', models.PositiveIntegerField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('message_id', djongo.models.fields.ObjectIdField(auto_created=True, primary_key=True, serialize=False)),
                ('registered_time', models.DateTimeField()),
                ('edited_time', models.DateTimeField()),
                ('is_read', models.BooleanField(default=False)),
                ('content', models.TextField(max_length=1000)),
                ('chat_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='users.chat')),
                ('sender_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='users.userprofile')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('comment_id', djongo.models.fields.ObjectIdField(auto_created=True, primary_key=True, serialize=False)),
                ('registered_time', models.DateTimeField()),
                ('edited_time', models.DateTimeField()),
                ('content', models.TextField(max_length=1000)),
                ('announcement_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='users.announcement')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='users.userprofile')),
            ],
        ),
        migrations.AddField(
            model_name='chat',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='users.userprofile'),
        ),
        migrations.AddField(
            model_name='announcement',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='users.userprofile'),
        ),
    ]