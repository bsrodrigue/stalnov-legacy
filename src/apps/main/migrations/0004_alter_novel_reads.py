# Generated by Django 3.2.7 on 2021-10-31 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0003_novel_reads"),
    ]

    operations = [
        migrations.AlterField(
            model_name="novel",
            name="reads",
            field=models.IntegerField(default=0),
        ),
    ]
