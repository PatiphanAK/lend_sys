# Generated by Django 5.1.1 on 2024-10-09 14:26

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("lend_app", "0003_alter_borrower_profile_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="approver",
            name="profile_image",
            field=models.ImageField(
                blank=True, null=True, upload_to="borrower_images/"
            ),
        ),
        migrations.AlterField(
            model_name="borrower",
            name="profile_image",
            field=models.ImageField(
                blank=True, null=True, upload_to="borrower_images/"
            ),
        ),
    ]
