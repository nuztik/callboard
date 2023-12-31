# Generated by Django 4.2.6 on 2023-10-09 12:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('context', models.TextField()),
                ('data', models.DateTimeField(auto_now_add=True)),
                ('category', models.CharField(choices=[('TN', 'Танки'), ('DD', 'ДД'), ('HL', 'Хиллы'), ('ME', 'Торговцы'), ('GM', 'Гилдмастера'), ('QG', 'Квестгиверы'), ('BS', 'Кузнецы'), ('TS', 'Кожевники'), ('PM', 'Зельевары'), ('SM', 'Мастера заклинаний')], max_length=2)),
                ('file', models.FileField(upload_to='media')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateTimeField(auto_now_add=True)),
                ('context', models.TextField()),
                ('accept', models.BooleanField(default=False)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='board.post')),
            ],
        ),
    ]
