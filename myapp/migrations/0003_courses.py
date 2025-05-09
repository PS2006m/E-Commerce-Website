# Generated by Django 5.1.5 on 2025-01-21 18:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_alter_user_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Courses',
            fields=[
                ('course_id', models.AutoField(primary_key=True, serialize=False)),
                ('course_name', models.CharField(max_length=100)),
                ('course_price', models.FloatField()),
                ('course_length', models.CharField(max_length=100)),
                ('course_img', models.ImageField(upload_to='media/course_images/')),
            ],
        ),
    ]
