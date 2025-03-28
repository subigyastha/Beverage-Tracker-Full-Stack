from django.db import models
from django.core.validators import MinValueValidator
from multiselectfield import MultiSelectField
from django.core.exceptions import ValidationError
import json

class BeverageEntry(models.Model):
    # Beverage Categories
    BEVERAGE_CATEGORIES = [
        ('water', 'Water-Based Beverages'),
        ('coffee', 'Coffee-Based Beverages'),
        ('tea', 'Tea-Based Beverages'),
        ('juice_smoothie', 'Juice & Smoothies'),
        ('dairy', 'Dairy-Based Beverages'),
        ('plant_milk', 'Plant-Based Milks'),
        ('fermented', 'Fermented & Probiotic Beverages'),
        ('carbonated', 'Carbonated & Artificially Sweetened Drinks'),
        ('alcohol', 'Alcoholic Beverages'),
        ('other', 'Other')
    ]

    # Detailed Subcategories
    BEVERAGE_SUBCATEGORIES = {
        'water': [
            ('plain_water', 'Plain Water'),
            ('infused_water', 'Infused Water (Lemon, Cucumber, Mint, Ginger)'),
            ('coconut_water', 'Coconut Water'),
            ('electrolyte_water', 'Electrolyte-Infused Water'),
            ('oral_rehydration', 'Oral Rehydration Solutions')
        ],
        'coffee': [
            ('black_coffee', 'Black Coffee'),
            ('espresso', 'Espresso'),
            ('americano', 'Americano'),
            ('cold_brew', 'Cold Brew'),
            ('latte_dairy', 'Latte (Dairy-Based)'),
            ('latte_plant', 'Latte (Plant-Based)'),
            ('cappuccino', 'Cappuccino'),
            ('mocha', 'Mocha')
        ],
        'tea': [
            ('green_tea', 'Green Tea'),
            ('black_tea', 'Black Tea'),
            ('white_tea', 'White Tea'),
            ('oolong_tea', 'Oolong Tea'),
            ('herbal_tea', 'Herbal Tea (Peppermint, Chamomile, Ginger, Fennel, Licorice Root)'),
            ('matcha', 'Matcha'),
            ('yerba_mate', 'Yerba Mate')
        ],
        'juice_smoothie': [
            ('fresh_fruit_juice', 'Fresh Fruit Juice (Apple, Orange, Pomegranate, etc.)'),
            ('vegetable_juice', 'Vegetable Juice (Carrot, Beet, Celery, etc.)'),
            ('fruit_smoothie', 'Blended Smoothies (Fruit-Based)'),
            ('vegetable_smoothie', 'Blended Smoothies (Vegetable-Based)')
        ],
        'dairy': [
            ('whole_milk', 'Whole Milk'),
            ('low_fat_milk', 'Low-Fat Milk'),
            ('skim_milk', 'Skim Milk'),
            ('lactose_free_milk', 'Lactose-Free Milk'),
            ('kefir', 'Kefir'),
            ('buttermilk', 'Buttermilk')
        ],
        'plant_milk': [
            ('almond_milk_unsweetened', 'Almond Milk (Unsweetened)'),
            ('almond_milk_sweetened', 'Almond Milk (Sweetened)'),
            ('oat_milk_unsweetened', 'Oat Milk (Unsweetened)'),
            ('oat_milk_sweetened', 'Oat Milk (Sweetened)'),
            ('soy_milk', 'Soy Milk'),
            ('coconut_milk', 'Coconut Milk'),
            ('rice_milk', 'Rice Milk'),
            ('hemp_milk', 'Hemp Milk')
        ],
        'fermented': [
            ('kombucha', 'Kombucha'),
            ('lassi', 'Lassi'),
            ('yakult', 'Yakult'),
            ('kvass', 'Kvass')
        ],
        'carbonated': [
            ('regular_soda', 'Regular Soda'),
            ('diet_soda', 'Diet Soda'),
            ('sparkling_water', 'Sparkling Water'),
            ('energy_drinks', 'Energy Drinks'),
            ('sports_drinks', 'Sports Drinks (Gatorade, Powerade)')
        ],
        'alcohol': [
            ('beer', 'Beer'),
            ('wine', 'Wine'),
            ('cider', 'Cider'),
            ('cocktails', 'Cocktails'),
            ('liquor', 'Liquor (Vodka, Whiskey, Gin, Tequila)')
        ],
        'other': [
            ('custom', 'Custom Entry')
        ]
    }

    # Temperature Choices
    TEMPERATURE_CHOICES = [
        ('ice_cold', 'Ice Cold (0°C / 32°F)'),
        ('chilled', 'Chilled (4°C / 40°F)'),
        ('cool', 'Cool (10°C / 50°F)'),
        ('room_temp', 'Room Temperature (20°C / 68°F)'),
        ('warm', 'Warm (50°C / 122°F)'),
        ('hot', 'Hot (70°C / 158°F)'),
        ('boiling', 'Boiling (100°C / 212°F)')
    ]

    # Unit Choices with Additional Options
    UNIT_CHOICES = [
        # Imperial Units
        ('fl_oz', 'Fluid Ounces'),
        ('cup', 'Cups'),
        ('pint', 'Pints'),
        ('quart', 'Quarts'),

        # Metric Units
        ('ml', 'Milliliters'),
        ('l', 'Liters'),

        # Other Specific Units
        ('shot', 'Shot'),
        ('can', 'Can'),
        ('bottle', 'Bottle')
    ]

    # Core Entry Fields
    date = models.DateField()
    time = models.TimeField()

    # Category and Subcategory with Custom Input
    category = models.CharField(
        max_length=50,
        choices=BEVERAGE_CATEGORIES
    )

    subcategory = models.CharField(
        max_length=100,
        blank=True,
        null=True  # Allow empty values
    )

    # Custom input fields for categories and subcategories
    custom_category = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Use only if 'Other' is selected"
    )

    custom_subcategory = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Custom subcategory if not in predefined list"
    )

    # Quantity with Custom Unit Support
    quantity = models.FloatField(
        validators=[MinValueValidator(0)],
        help_text="Numeric quantity of the beverage"
    )

    unit = models.CharField(
        max_length=20,
        choices=UNIT_CHOICES
    )

    custom_unit = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="Custom unit if not in predefined list"
    )

    # Temperature
    temperature = models.CharField(
        max_length=20,
        choices=TEMPERATURE_CHOICES
    )

   
    notes = models.TextField(
        blank=True,
        null=True,
        help_text="Additional notes about the beverage"
    )

    has_symptoms = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.category} - {self.subcategory or self.custom_subcategory} ({self.date})"

    def clean(self):
        super().clean()
        if self.category and self.subcategory:
            valid_subcategories = self.BEVERAGE_SUBCATEGORIES.get(self.category, [])
            valid_subcategory_values = [sc[0] for sc in valid_subcategories]
            if self.category != 'other' and self.subcategory not in valid_subcategory_values:
                raise ValidationError({
                    'subcategory': f"Invalid subcategory '{self.subcategory}' for {self.get_category_display()}"
                })
                
    def save(self, *args, **kwargs):
        self.clean()
        if self.category != 'other':
            self.custom_category = None
        if self.subcategory:
            self.custom_subcategory = None
        super().save(*args, **kwargs)

class Symptoms(models.Model):
    SYMPTOMS_CHOICES = [
        ('Bloating', 'Bloating'),
        ('Discomfort', 'Discomfort'),
        ('Nausea', 'Nausea'),
        ('Acid Reflux / Heartburn', 'Acid Reflux / Heartburn'),
        ('Burping / Excess Gas', 'Burping / Excess Gas'),
        ('Diarrhea / Loose Stools', 'Diarrhea / Loose Stools'),
        ('Constipation', 'Constipation'),
        ('Cramping / Abdominal Pain', 'Cramping / Abdominal Pain'),
        ('Urgency to Poop', 'Urgency to Poop'),
        ('Mucus in Stool', 'Mucus in Stool'),
        ('Fatty / Oily Stools (Steatorrhea)', 'Fatty / Oily Stools (Steatorrhea)'),
        ('Undigested Food in Stool', 'Undigested Food in Stool'),
        ('Feeling Full / Heavy Stomach', 'Feeling Full / Heavy Stomach'),
        ('Dizziness / Lightheadedness', 'Dizziness / Lightheadedness'),
        ('Headache', 'Headache'),
        ('Dry Mouth / Sticky Saliva', 'Dry Mouth / Sticky Saliva'),
        ('others','Others')]

    SYMPTOMS_SEVERITY = [
        ('Mild', 'Mild'),
        ('Moderate', 'Moderate'),
        ('Severe', 'Severe'),
    ]

    SYMPTOMS_TIMING = [
        ('Mild', 'Immediately'),
        ('20-30', 'Within 20 to 30 Minutes'),
        ('2-5', '2 to 5 hours'),
        ('5+', '5+ hours later'),
    ]

    beverage_entry = models.ForeignKey(
        BeverageEntry,
        on_delete=models.CASCADE,
        related_name='symptoms',
        blank=True,
        null=True
    )
    symptoms = models.CharField(
        max_length=50,
        blank=False,
        null=False,
        choices=SYMPTOMS_CHOICES
    )
    custom_symptoms = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="Custom symptom if not in predefined list"
    )
    severity = models.CharField(
        max_length=8,
        blank=False,
        null=False,
        choices=SYMPTOMS_SEVERITY
    )
    timing = models.CharField(
        max_length=5,
        blank=False,
        null=False,
        choices=SYMPTOMS_TIMING
    )

    def save(self, *args, **kwargs):
        if self.symptoms != 'others':
            self.custom_symptoms = None
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.get_symptoms_display()} - {self.get_severity_display()} - {self.get_timing_display()}"
    




class Additives(models.Model):
    beverage_entry = models.ForeignKey(
        BeverageEntry,
        on_delete=models.CASCADE,
        related_name='additives',
        blank=True,
        null=True
    )
    ADDITIVES_CHOICES = [
        ('sugar', 'Sugar'),
        ('milk', 'Milk'),
        ('cream', 'Cream'),
        ('lime', 'Lime'),
        ('honey', 'Honey'),
        ('artificial_sweeteners', 'Artificial Sweeteners'),
        ('protein_powders', 'Protein Powders'),
        ('electrolyte_powders', 'Electrolyte Powders'),
        ('others','Others')
    ]

    name = models.CharField(
        max_length=50,
        blank=False,
        null=False,
        choices=ADDITIVES_CHOICES
    )

    custom_additives = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="Specify if the additive is not listed above."    )

    

    def __str__(self):
        return self.name

    