# Generated by Django 4.1.4 on 2023-05-02 09:43

import Q_app.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="clientdetails",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("clientname", models.CharField(max_length=50)),
                ("username", models.CharField(max_length=50)),
                ("password", models.BinaryField(max_length=100)),
                ("email", models.CharField(max_length=100)),
                ("date", models.CharField(max_length=50)),
                ("image", models.ImageField(upload_to=Q_app.models.upload_path)),
                ("role", models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name="logindetails",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("username", models.CharField(max_length=20)),
                ("password", models.CharField(max_length=20)),
                ("role", models.CharField(max_length=20)),
                ("mail", models.EmailField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name="requirements",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("campaign_name", models.CharField(max_length=100)),
                ("start_date", models.CharField(max_length=100)),
                ("end_date", models.CharField(max_length=100)),
                ("planned_impressions", models.CharField(max_length=100)),
                ("planned_cpm", models.CharField(max_length=100)),
                ("planned_cpc", models.CharField(max_length=100)),
                ("planned_cost", models.CharField(max_length=100)),
                (
                    "deptid",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Q_app.clientdetails",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="user_report",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("clientname", models.CharField(max_length=100)),
                ("campaign_name", models.CharField(max_length=100)),
                ("date", models.CharField(max_length=10)),
                ("no_of_impressions", models.IntegerField()),
                ("no_of_clicks", models.IntegerField()),
                ("cost_per_impressions", models.IntegerField()),
                ("cost_per_click", models.IntegerField()),
                ("total_cost_per_impressions", models.IntegerField()),
                ("total_cost_per_click", models.IntegerField()),
                ("cost_per_day", models.IntegerField()),
                (
                    "clientid",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Q_app.requirements",
                    ),
                ),
            ],
        ),
    ]
