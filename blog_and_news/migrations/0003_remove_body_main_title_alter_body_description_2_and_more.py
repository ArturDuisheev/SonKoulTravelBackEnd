# Generated by Django 4.1.7 on 2023-05-09 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog_and_news', '0002_blog_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='body',
            name='main_title',
        ),
        migrations.AlterField(
            model_name='body',
            name='description_2',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='body',
            name='description_3',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='body',
            name='description_4',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='body',
            name='quote',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='body',
            name='title_2',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='body',
            name='title_3',
            field=models.CharField(max_length=255),
        ),
    ]
