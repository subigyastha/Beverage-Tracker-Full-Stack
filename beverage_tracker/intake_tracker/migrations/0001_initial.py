# Generated by Django 5.1.7 on 2025-03-26 19:48

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BeverageEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('category', models.CharField(choices=[('water', 'Water-Based Beverages'), ('coffee', 'Coffee-Based Beverages'), ('tea', 'Tea-Based Beverages'), ('juice_smoothie', 'Juice & Smoothies'), ('dairy', 'Dairy-Based Beverages'), ('plant_milk', 'Plant-Based Milks'), ('fermented', 'Fermented & Probiotic Beverages'), ('carbonated', 'Carbonated & Artificially Sweetened Drinks'), ('alcohol', 'Alcoholic Beverages'), ('other', 'Other')], max_length=50)),
                ('subcategory', models.CharField(blank=True, choices=[], max_length=100)),
                ('custom_category', models.CharField(blank=True, help_text="Use only if 'Other' is selected", max_length=100, null=True)),
                ('custom_subcategory', models.CharField(blank=True, help_text='Custom subcategory if not in predefined list', max_length=100, null=True)),
                ('quantity', models.FloatField(help_text='Numeric quantity of the beverage', validators=[django.core.validators.MinValueValidator(0)])),
                ('unit', models.CharField(choices=[('fl_oz', 'Fluid Ounces'), ('cup', 'Cups'), ('pint', 'Pints'), ('quart', 'Quarts'), ('ml', 'Milliliters'), ('l', 'Liters'), ('shot', 'Shot'), ('can', 'Can'), ('bottle', 'Bottle')], max_length=20)),
                ('custom_unit', models.CharField(blank=True, help_text='Custom unit if not in predefined list', max_length=50, null=True)),
                ('temperature', models.CharField(choices=[('ice_cold', 'Ice Cold (0°C / 32°F)'), ('chilled', 'Chilled (4°C / 40°F)'), ('cool', 'Cool (10°C / 50°F)'), ('room_temp', 'Room Temperature (20°C / 68°F)'), ('warm', 'Warm (50°C / 122°F)'), ('hot', 'Hot (70°C / 158°F)'), ('boiling', 'Boiling (100°C / 212°F)')], max_length=20)),
                ('additives', models.JSONField(blank=True, help_text='JSON object of additional ingredients', null=True)),
                ('notes', models.TextField(blank=True, help_text='Additional notes about the beverage', null=True)),
                ('has_symptoms', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Symptoms',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symptoms', models.CharField(choices=[('Bloating', 'Bloating'), ('Discomfort', 'Discomfort'), ('Nausea', 'Nausea'), ('Acid Reflux / Heartburn', 'Acid Reflux / Heartburn'), ('Burping / Excess Gas', 'Burping / Excess Gas'), ('Diarrhea / Loose Stools', 'Diarrhea / Loose Stools'), ('Constipation', 'Constipation'), ('Cramping / Abdominal Pain', 'Cramping / Abdominal Pain'), ('Urgency to Poop', 'Urgency to Poop'), ('Mucus in Stool', 'Mucus in Stool'), ('Fatty / Oily Stools (Steatorrhea)', 'Fatty / Oily Stools (Steatorrhea)'), ('Undigested Food in Stool', 'Undigested Food in Stool'), ('Feeling Full / Heavy Stomach', 'Feeling Full / Heavy Stomach'), ('Dizziness / Lightheadedness', 'Dizziness / Lightheadedness'), ('Headache', 'Headache'), ('Dry Mouth / Sticky Saliva', 'Dry Mouth / Sticky Saliva'), ('others', 'Others')], max_length=50)),
                ('custom_symptoms', models.CharField(blank=True, help_text='Custom symptom if not in predefined list', max_length=50, null=True)),
                ('severity', models.CharField(choices=[('Mild', 'Mild'), ('Moderate', 'Moderate'), ('Severe', 'Severe')], max_length=8)),
                ('timing', models.CharField(choices=[('Mild', 'Immediately'), ('20-30', 'Within 20 to 30 Minutes'), ('2-5', '2 to 5 hours'), ('5+', '5+ hours later')], max_length=5)),
                ('beverage_entry', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='symptoms', to='intake_tracker.beverageentry')),
            ],
        ),
    ]
