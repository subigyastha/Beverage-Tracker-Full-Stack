from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    DetailView
)
from django.urls import reverse, reverse_lazy
from django.contrib import messages

from .models import BeverageEntry, Additives, Symptoms  # Import Additives
from .forms import AdditiveFormSet, SymptomFormSet,BeverageEntryForm

class BeverageEntryListView(ListView):
    model = BeverageEntry
    template_name = 'beverage_entry_list.html'
    context_object_name = 'entries'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()

        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category=category)

        return queryset.order_by('-date', '-time')

class BeverageEntryDetailView(DetailView):
    model = BeverageEntry
    template_name = 'beverage_entry_detail.html'
    context_object_name = 'entry'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['additives'] = self.object.additives.all()  # Get related additives
        context['symptoms'] = self.object.additives.all()  # Get related additives
        return context

class BeverageEntryCreateView(CreateView):
    model = BeverageEntry
    form_class = BeverageEntryForm
    template_name = 'beverage_entry_form.html'
    success_url = reverse_lazy('beverage_entry_list')

    def form_valid(self, form):
        messages.success(self.request, 'Beverage entry created successfully.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = BeverageEntry.BEVERAGE_CATEGORIES
        context['subcategories'] = BeverageEntry.BEVERAGE_SUBCATEGORIES
        return context

from django.views.generic import UpdateView
from django.urls import reverse_lazy

class BeverageEntryUpdateView(UpdateView):
    model = BeverageEntry
    form_class = BeverageEntryForm
    template_name = 'beverage/beverage_entry_form.html'
    
    def get_success_url(self):
        return reverse('beverage_entry_detail', kwargs={'pk': self.object.pk})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['additive_formset'] = AdditiveFormSet(
                self.request.POST,
                instance=self.object,
                prefix='additives'
            )
            context['symptom_formset'] = SymptomFormSet(
                self.request.POST,
                instance=self.object,
                prefix='symptoms'
            )
        else:
            context['additive_formset'] = AdditiveFormSet(
                instance=self.object,
                prefix='additives'
            )
            context['symptom_formset'] = SymptomFormSet(
                instance=self.object,
                prefix='symptoms'
            )
        return context
    
    def form_valid(self, form):
        context = self.get_context_data()
        additive_formset = context['additive_formset']
        symptom_formset = context['symptom_formset']
        
        if additive_formset.is_valid() and symptom_formset.is_valid():
            self.object = form.save()
            additive_formset.instance = self.object
            additive_formset.save()
            
            if self.object.has_symptoms:
                symptom_formset.instance = self.object
                symptom_formset.save()
            else:
                # Delete all symptoms if has_symptoms is unchecked
                self.object.symptoms.all().delete()
            
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))
class BeverageEntryDeleteView(DeleteView):
    model = BeverageEntry
    template_name = 'beverage_entry_confirm_delete.html'
    success_url = reverse_lazy('beverage_entry_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Beverage entry deleted successfully.')
        return super().delete(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['additives'] = self.object.additives.all()  # Get related additives
        context['symptoms'] = self.object.additives.all()  # Get related additives
        return context

# Optional: Advanced filtering view (remains largely the same)
def beverage_entry_filter(request):
    queryset = BeverageEntry.objects.all()

    category = request.GET.get('category')
    if category:
        queryset = queryset.filter(category=category)

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    if start_date and end_date:
        queryset = queryset.filter(date__range=[start_date, end_date])

    has_symptoms = request.GET.get('has_symptoms')
    if has_symptoms:
        queryset = queryset.filter(has_symptoms=True)

    return render(request, 'beverage_entry_filter.html', {
        'entries': queryset,
        'categories': BeverageEntry.BEVERAGE_CATEGORIES
    })

def create_beverage_entry(request):
    if request.method == 'POST':
        beverage_form = BeverageEntryForm(request.POST)
        additive_formset = AdditiveFormSet(request.POST, prefix='additives')
        symptom_formset = SymptomFormSet(request.POST, prefix='symptoms')

        print("POST data:", request.POST)
        print("Beverage form valid:", beverage_form.is_valid())
        if not beverage_form.is_valid():
            print("Beverage form errors:", beverage_form.errors)

        if (beverage_form.is_valid() and 
            additive_formset.is_valid() and 
            symptom_formset.is_valid()):
            
            has_symptoms = any(
                form.cleaned_data and not form.cleaned_data.get('DELETE', False)
                for form in symptom_formset
            )
            
            beverage = beverage_form.save(commit=False)
            beverage.has_symptoms = has_symptoms
            beverage.save()
            
            for form in additive_formset:
                if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                    name = form.cleaned_data['name']
                    custom_additive = form.cleaned_data['custom_additives']
                    Additives.objects.create(
                        beverage_entry=beverage,
                        name=name if name != 'others' else custom_additive,
                        custom_additives=custom_additive if name == 'others' else ''
                    )
            
            if has_symptoms:
                for form in symptom_formset:
                    if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                        symptom = form.cleaned_data['symptoms']
                        custom_symptom = form.cleaned_data['custom_symptoms']
                        Symptoms.objects.create(
                            beverage_entry=beverage,
                            symptoms=symptom if symptom != 'others' else custom_symptom,
                            custom_symptoms=custom_symptom if symptom == 'others' else '',
                            severity=form.cleaned_data['severity'],
                            timing=form.cleaned_data['timing']
                        )
            
            messages.success(request, 'Beverage entry created successfully.')
            return redirect('beverage_entry_detail', pk=beverage.pk)
    else:
        beverage_form = BeverageEntryForm()
        additive_formset = AdditiveFormSet(prefix='additives', queryset=Additives.objects.none())
        symptom_formset = SymptomFormSet(prefix='symptoms', queryset=Symptoms.objects.none())

    context = {
        'beverage_form': beverage_form,
        'additive_formset': additive_formset,
        'symptom_formset': symptom_formset,
    }
    return render(request, 'beverage_entry_form.html', context)


from django.contrib import messages

def edit_beverage_entry(request, pk):
    beverage = BeverageEntry.objects.get(pk=pk)
    if request.method == 'POST':
        beverage_form = BeverageEntryForm(request.POST, instance=beverage)
        additive_formset = AdditiveFormSet(request.POST, instance=beverage, prefix='additives')
        symptom_formset = SymptomFormSet(request.POST, instance=beverage, prefix='symptoms')

        print("POST request received")
        print("POST data:", request.POST)
        print("Beverage form valid:", beverage_form.is_valid())
        if not beverage_form.is_valid():
            print("Beverage form errors:", beverage_form.errors)
            messages.error(request, "Beverage form has errors: " + str(beverage_form.errors.as_text()))
        print("Additive formset valid:", additive_formset.is_valid())
        if not additive_formset.is_valid():
            print("Additive formset errors:", additive_formset.errors)
            # Construct a detailed error message for additives
            additive_errors = []
            for i, form_errors in enumerate(additive_formset.errors):
                if form_errors:
                    additive_errors.append(f"Additive {i + 1}: {str(form_errors.as_text())}")
            if additive_errors:
                messages.error(request, "Additive formset has errors: " + "; ".join(additive_errors))
            else:
                messages.error(request, "Additive formset failed validation, but no specific errors found.")
        print("Symptom formset valid:", symptom_formset.is_valid())
        if not symptom_formset.is_valid():
            print("Symptom formset errors:", symptom_formset.errors)
            symptom_errors = []
            for i, form_errors in enumerate(symptom_formset.errors):
                if form_errors:
                    symptom_errors.append(f"Symptom {i + 1}: {str(form_errors.as_text())}")
            if symptom_errors:
                messages.error(request, "Symptom formset has errors: " + "; ".join(symptom_errors))
            else:
                messages.error(request, "Symptom formset failed validation, but no specific errors found.")

        if (beverage_form.is_valid() and 
            additive_formset.is_valid() and 
            symptom_formset.is_valid()):
            
            has_symptoms = any(
                form.cleaned_data and not form.cleaned_data.get('DELETE', False)
                for form in symptom_formset
            )
            
            beverage = beverage_form.save(commit=False)
            beverage.has_symptoms = has_symptoms
            beverage.save()
            
            additive_formset.save()
            symptom_formset.save()
            
            messages.success(request, 'Beverage entry updated successfully.')
            return redirect('beverage_entry_detail', pk=beverage.pk)
        else:
            messages.error(request, "Form submission failed. Please check the errors below.")
    else:
        beverage_form = BeverageEntryForm(instance=beverage)
        additive_formset = AdditiveFormSet(instance=beverage, prefix='additives')
        symptom_formset = SymptomFormSet(instance=beverage, prefix='symptoms')

    context = {
        'beverage_form': beverage_form,
        'additive_formset': additive_formset,
        'symptom_formset': symptom_formset,
        'editing': True,
    }
    return render(request, 'beverage_entry_form.html', context)