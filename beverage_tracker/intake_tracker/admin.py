from django.contrib import admin
from .models import BeverageEntry, Symptoms, Additives


class AdditivesInline(admin.TabularInline):
    model = Additives
    extra = 1
    fields = ('name', 'custom_additives')

class SymptomsInline(admin.TabularInline):
    model = Symptoms
    extra = 1
    fields = ('symptoms', 'custom_symptoms', 'severity', 'timing')

class BeverageEntryAdmin(admin.ModelAdmin):
    inlines = [SymptomsInline, AdditivesInline]
    list_display = ('date', 'time', 'category', 'subcategory', 'quantity', 'unit', 'has_symptoms')
    list_filter = ('category', 'date', 'has_symptoms')
    search_fields = ('category', 'subcategory', 'custom_category', 'custom_subcategory', 'notes')

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        obj.has_symptoms = obj.symptoms.exists()
        obj.save()

    def has_symptoms(self, obj):
        return obj.symptoms.exists()
    has_symptoms.boolean = True
    has_symptoms.short_description = 'Has Symptoms'

admin.site.register(BeverageEntry, BeverageEntryAdmin)
admin.site.register(Symptoms)
admin.site.register(Additives)