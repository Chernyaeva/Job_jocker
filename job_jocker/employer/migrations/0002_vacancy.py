# Generated by Django 4.2.6 on 2023-10-11 22:04

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('employer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vacancy',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('profession', models.CharField(max_length=100)),
                ('experience', models.TextField(blank=True, null=True)),
                ('skills', models.TextField(blank=True, null=True)),
                ('education', models.CharField(max_length=100)),
                ('salary', models.IntegerField(blank=True, default=0, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('address', models.CharField(max_length=300)),
                ('inn', models.IntegerField(blank=True, default=0, null=True)),
                ('is_posted', models.BooleanField(default=False, null=True)),
                ('admin_comment', models.TextField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('card_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employer.card')),
            ],
        ),
    ]
