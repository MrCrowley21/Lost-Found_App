# Generated by Django 3.2.16 on 2022-12-04 18:36

import databaseQueries.models
import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', databaseQueries.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('register_date', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('close_date', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(blank=True, max_length=20)),
                ('location', models.CharField(blank=True, max_length=10)),
                ('credit_details', models.CharField(blank=True, max_length=16)),
                ('image', models.ImageField(blank=True, upload_to='IMG/')),
                ('rating', models.PositiveIntegerField(blank=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('registered_time', models.DateTimeField(default=datetime.datetime.now)),
                ('edited_time', models.DateTimeField()),
                ('is_read', models.BooleanField(default=False)),
                ('content', models.TextField(max_length=1000)),
                ('chat_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='databaseQueries.chat')),
                ('sender_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='databaseQueries.userprofile')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('registered_time', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('edited_time', models.DateTimeField()),
                ('content', models.TextField(max_length=1000)),
                ('announcement_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='databaseQueries.comment')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='databaseQueries.userprofile')),
            ],
        ),
        migrations.AddField(
            model_name='chat',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='databaseQueries.userprofile'),
        ),
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('location', models.URLField(max_length=250)),
                ('image', models.ImageField(blank=True, upload_to='IMGS/')),
                ('annType', models.CharField(max_length=5)),
                ('content', models.TextField(max_length=5000)),
                ('reward', models.PositiveSmallIntegerField(blank=True, default=0)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('passed_time', models.CharField(max_length=50)),
                ('tags', models.ManyToManyField(to='databaseQueries.Tag')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='databaseQueries.userprofile')),
            ],
        ),
    ]
