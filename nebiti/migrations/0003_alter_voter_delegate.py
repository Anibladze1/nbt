# Generated by Django 4.1.5 on 2023-02-22 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("nebiti", "0002_alter_voter_delegated_to"),
    ]

    operations = [
        migrations.AlterField(
            model_name="voter",
            name="delegate",
            field=models.ManyToManyField(blank=True, to="nebiti.voter"),
        ),
    ]