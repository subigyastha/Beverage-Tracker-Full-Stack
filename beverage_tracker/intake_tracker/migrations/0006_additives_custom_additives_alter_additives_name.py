# Generated by Django 5.1.7 on 2025-03-26 21:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('intake_tracker', '0005_remove_beverageentry_additives_additives'),
    ]

    operations = [
        migrations.AddField(
            model_name='additives',
            name='custom_additives',
            field=models.CharField(blank=True, help_text='Custom symptom if not in predefined list', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='additives',
            name='name',
            field=models.CharField(choices=[('sugar', 'Sugar'), ('milk', 'Milk'), ('cream', 'Cream'), ('lime', 'Lime'), ('honey', 'Honey'), ('artificial_sweeteners', 'Artificial Sweeteners'), ('protein_powders', 'Protein Powders'), ('electrolyte_powders', 'Electrolyte Powders'), ('others', 'Others')], max_length=50),
        ),
    ]
