
# Generated by Django 4.2.6 on 2023-10-12 17:34

from django.db import migrations, models
import django.db.models.deletion




class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[

                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('mail', models.CharField(max_length=100)),
                ('legal_form', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('address', models.CharField(max_length=300)),
                ('inn', models.IntegerField(blank=True, default=0, null=True)),
                ('web_site', models.CharField(max_length=100)),
                ('logo', models.ImageField(blank=True, default='logo_images/default_logo.jpg', null=True, upload_to='profile_images')),
                ('is_posted', models.BooleanField(default=False, null=True)),
                ('admin_comment', models.TextField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),

        migrations.CreateModel(
            name='Vacancy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profession', models.CharField(max_length=100)),
                ('experience', models.TextField(blank=True, null=True)),
                ('skills', models.TextField(blank=True, null=True)),
                ('education', models.CharField(max_length=100)),
                ('salary', models.IntegerField(blank=True, default=0, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('address', models.CharField(max_length=300)),
                ('is_posted', models.BooleanField(default=False, null=True)),
                ('admin_comment', models.TextField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('card_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employer.card')),
            ],
        ),
    ]