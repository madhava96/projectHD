# Generated by Django 4.1.4 on 2023-05-30 04:19

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Q_app", "0003_alter_requirements_planned_cost_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="requirements",
            name="planned_cost",
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name="requirements",
            name="planned_cpc",
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name="requirements",
            name="planned_cpm",
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name="requirements",
            name="planned_impressions",
            field=models.CharField(max_length=100),
        ),
    ]
