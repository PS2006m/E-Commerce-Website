# Generated by Django 5.1.5 on 2025-02-21 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0008_cart'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courses',
            name='course_bought',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
