# Generated by Django 3.2.5 on 2021-07-28 19:40

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='blogs',
            managers=[
                ('object', django.db.models.manager.Manager()),
            ],
        ),
        migrations.RenameField(
            model_name='blogs',
            old_name='author',
            new_name='author_id',
        ),
    ]