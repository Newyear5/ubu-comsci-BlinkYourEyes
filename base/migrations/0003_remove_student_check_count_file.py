# Generated by Django 4.0.4 on 2022-06-08 14:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_student_check_count_file'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student_check_count',
            name='file',
        ),
    ]