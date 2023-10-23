# Generated by Django 3.2.22 on 2023-10-23 06:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('applicant', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(max_length=300)),
                ('response', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('mail', models.EmailField(max_length=100)),
                ('legal_form', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('address', models.CharField(max_length=300)),
                ('inn', models.IntegerField(default=0)),
                ('phone', models.CharField(max_length=20)),
                ('web_site', models.CharField(max_length=100)),
                ('logo', models.ImageField(default='logo_images/default_logo.jpg', upload_to='profile_images')),
                ('is_posted', models.BooleanField(default=False, null=True)),
                ('admin_comment', models.TextField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('role', models.CharField(default='employer', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Vacancy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profession', models.CharField(max_length=100)),
                ('experience', models.TextField()),
                ('skills', models.TextField()),
                ('education', models.CharField(max_length=100)),
                ('salary', models.IntegerField()),
                ('description', models.TextField()),
                ('address', models.CharField(max_length=300)),
                ('is_posted', models.BooleanField(default=False)),
                ('admin_comment', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('card_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employer.card')),
            ],
        ),
        migrations.CreateModel(
            name='FavoriteResumes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('card', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employer.card')),
                ('resume', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='applicant.resume')),
            ],
        ),
    ]
