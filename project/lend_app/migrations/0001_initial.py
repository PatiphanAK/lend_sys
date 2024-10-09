# Generated by Django 5.1.1 on 2024-10-09 09:00

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Category",
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
                ("name", models.CharField(max_length=100, unique=True)),
                ("description", models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name="EquipmentStock",
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
                ("quantity", models.PositiveIntegerField()),
                ("available", models.PositiveIntegerField(default=0)),
                ("is_available", models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name="Organization",
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
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("GOV", "Government"),
                            ("EDU", "Educational"),
                            ("CORP", "Corporate"),
                        ],
                        max_length=4,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Approver",
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
                ("description", models.TextField(blank=True)),
                (
                    "profile_image",
                    models.ImageField(
                        blank=True, null=True, upload_to="approver_images/"
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "organization",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="lend_app.organization",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Borrower",
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
                (
                    "profile_image",
                    models.ImageField(
                        blank=True, null=True, upload_to="borrower_images/"
                    ),
                ),
                ("description", models.TextField(blank=True)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="BorrowRequest",
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
                ("quantity", models.PositiveIntegerField()),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("PENDING", "Pending"),
                            ("APPROVED", "Approved"),
                            ("REJECTED", "Rejected"),
                            ("RETURNED", "Returned"),
                        ],
                        default="PENDING",
                        max_length=10,
                    ),
                ),
                ("borrow_date", models.DateField(auto_now_add=True)),
                ("return_date", models.DateField(blank=True, null=True)),
                (
                    "approver",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="lend_app.approver",
                    ),
                ),
                (
                    "borrower",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="lend_app.borrower",
                    ),
                ),
                (
                    "equipment_stock",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="lend_app.equipmentstock",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Item",
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
                ("description", models.TextField(blank=True)),
                (
                    "item_image",
                    models.ImageField(blank=True, null=True, upload_to="item_images/"),
                ),
                (
                    "categories",
                    models.ManyToManyField(
                        related_name="items", to="lend_app.category"
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="equipmentstock",
            name="item",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="lend_app.item"
            ),
        ),
        migrations.AddField(
            model_name="equipmentstock",
            name="organization",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="lend_app.organization"
            ),
        ),
        migrations.CreateModel(
            name="BorrowQueue",
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
                ("queue_position", models.PositiveIntegerField()),
                ("request_date", models.DateField(auto_now_add=True)),
                ("quantity", models.PositiveIntegerField()),
                (
                    "borrower",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="lend_app.borrower",
                    ),
                ),
                (
                    "equipment_stock",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="lend_app.equipmentstock",
                    ),
                ),
            ],
            options={
                "constraints": [
                    models.UniqueConstraint(
                        fields=("equipment_stock", "queue_position"),
                        name="unique_queue_position",
                    )
                ],
            },
        ),
    ]
