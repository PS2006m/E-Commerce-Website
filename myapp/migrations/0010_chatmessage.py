# Generated by Django 5.1.5 on 2025-03-07 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0009_alter_courses_course_bought'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChatMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=255)),
                ('message', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
