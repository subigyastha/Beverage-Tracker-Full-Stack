from django import forms
from django.forms import inlineformset_factory
from .models import BeverageEntry, Symptoms, Additives

class BeverageEntryForm(forms.ModelForm):
    class Meta:
        model = BeverageEntry
        fields = ['date', 'time', 'category', 'subcategory', 'custom_category', 
                  'custom_subcategory', 'quantity', 'unit', 'custom_unit', 'temperature', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500', 'required': 'required'}),
            'time': forms.TimeInput(attrs={'type': 'time', 'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500', 'required': 'required'}),
            'category': forms.Select(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 custom-select-arrow'}),
            'subcategory': forms.Select(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 custom-select-arrow'}),
            'custom_category': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500', 'placeholder': 'Enter custom category if "Other" selected'}),
            'custom_subcategory': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500', 'placeholder': 'Enter custom subcategory if "Other" selected'}),
            'quantity': forms.NumberInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500', 'step': '0.1', 'min': '0', 'placeholder': 'e.g., 250'}),
            'unit': forms.Select(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 custom-select-arrow'}),
            'custom_unit': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500', 'placeholder': 'Enter custom unit if "Other" selected'}),
            'temperature': forms.Select(attrs={'class': 'w-full temperature-slider hidden'}),
            'notes': forms.Textarea(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500', 'rows': 3, 'placeholder': 'Additional notes (optional)'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        category = self.data.get('category') if self.data else self.instance.category if self.instance.pk else None
        print(f"Form init - Category: {category}, Instance: {self.instance.pk if self.instance else 'None'}")
        print(f"Initial subcategory from instance: {self.instance.subcategory if self.instance else 'None'}")

        if category in BeverageEntry.BEVERAGE_SUBCATEGORIES:
            self.fields['subcategory'].choices = BeverageEntry.BEVERAGE_SUBCATEGORIES[category]
        else:
            self.fields['subcategory'].choices = [('', '---------')]

        if self.instance and self.instance.subcategory:
            self.fields['subcategory'].initial = self.instance.subcategory  # Set field initial explicitly
            print(f"Set subcategory initial to: {self.instance.subcategory}")

        self.fields['subcategory'].required = False
        print(f"Subcategory choices: {self.fields['subcategory'].choices}")
        print(f"Subcategory initial: {self.fields['subcategory'].initial}")

    def clean(self):
        cleaned_data = super().clean()
        category = cleaned_data.get('category')
        subcategory = cleaned_data.get('subcategory')

        if category == 'other' and not subcategory and not cleaned_data.get('custom_subcategory'):
            self.add_error('custom_subcategory', "Please specify a custom subcategory when 'Other' is selected.")
        elif category != 'other' and subcategory:
            valid_subcategories = BeverageEntry.BEVERAGE_SUBCATEGORIES.get(category, [])
            valid_values = [sc[0] for sc in valid_subcategories]
            if subcategory not in valid_values:
                self.add_error('subcategory', f"Invalid subcategory '{subcategory}' for category '{category}'.")
        
        return cleaned_data

class AdditiveForm(forms.ModelForm):
    class Meta:
        model = Additives
        fields = ['name', 'custom_additives']
        widgets = {
            'name': forms.Select(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md'}),
            'custom_additives': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].required = False
        self.fields['custom_additives'].required = False

    def clean(self):
        cleaned_data = super().clean()
        # Skip validation if the form is marked for deletion
        if cleaned_data.get('DELETE', False):
            return cleaned_data  # No validation needed for deleted forms
        name = cleaned_data.get('name')
        custom_additives = cleaned_data.get('custom_additives')
        if not name and not custom_additives:
            raise forms.ValidationError("Either 'name' or 'custom additives' must be provided.")
        return cleaned_data



class SymptomForm(forms.ModelForm):
    class Meta:
        model = Symptoms
        fields = ['symptoms', 'custom_symptoms', 'severity', 'timing']
        widgets = {
            'symptoms': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 symptom-select custom-select-arrow',
            }),
            'custom_symptoms': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500',
                'placeholder': 'Specify custom symptom',
            }),
            'severity': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 custom-select-arrow',
            }),
            'timing': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 custom-select-arrow',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['symptoms'].required = False  # Allow blank, validate in clean()
        self.fields['custom_symptoms'].required = False
        self.fields['severity'].required = False
        self.fields['timing'].required = False

    def clean(self):
        cleaned_data = super().clean()
        # Skip validation if marked for deletion
        if cleaned_data.get('DELETE', False):
            return cleaned_data  # No validation for deleted forms
        symptoms = cleaned_data.get('symptoms')
        custom_symptoms = cleaned_data.get('custom_symptoms')
        # Require either symptoms or custom_symptoms, but only for non-deleted forms
        if not symptoms and not custom_symptoms:
            raise forms.ValidationError("Either 'symptoms' or 'custom symptoms' must be provided.")
        return cleaned_data

AdditiveFormSet = inlineformset_factory(
    BeverageEntry, Additives, form=AdditiveForm, extra=1, can_delete=True
)

SymptomFormSet = inlineformset_factory(
    BeverageEntry, Symptoms, form=SymptomForm, extra=1, can_delete=True
)