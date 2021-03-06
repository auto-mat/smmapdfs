# Generated by Django 2.2.7 on 2019-11-26 16:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("smmapdfs", "0002_auto_20180611_1830"),
    ]

    operations = [
        migrations.AddField(
            model_name="pdfsandwichabc",
            name="status",
            field=models.TextField(blank=True, default="", verbose_name="Status"),
        ),
        migrations.AlterField(
            model_name="pdfsandwichabc",
            name="pdfsandwich_type",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="smmapdfs.PdfSandwichType",
                verbose_name="PDF sandwich template/type",
            ),
        ),
        migrations.AlterField(
            model_name="pdfsandwichemail",
            name="language",
            field=models.CharField(
                choices=[("en", "English"), ("cs", "Czech"), ("dsnkcs", "Škola")],
                max_length=80,
                verbose_name="Language",
            ),
        ),
    ]
