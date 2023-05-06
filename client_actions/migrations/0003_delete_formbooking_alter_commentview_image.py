# Generated by Django 4.1.7 on 2023-05-06 13:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('client_actions', '0002_alter_commentview_image'),
    ]

    operations = [
        migrations.DeleteModel(
            name='FormBooking',
        ),
        migrations.AlterField(
            model_name='commentview',
            name='image',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Изображение', to='client_actions.commentimage', verbose_name='Изображение'),
        ),
    ]
