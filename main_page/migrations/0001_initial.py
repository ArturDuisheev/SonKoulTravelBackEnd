# Generated by Django 4.1.7 on 2023-05-13 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FormQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.TextField(verbose_name='Write your question')),
                ('contact', models.CharField(max_length=100, verbose_name='Leave your E-mail or WhatsApp')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]