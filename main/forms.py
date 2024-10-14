from django import forms
from .models import Sample_Metadata, Sample

class SampleFilterForm(forms.Form):
    # Dropdown for Cell Type
    cell_type = forms.ChoiceField(
        choices=[('', 'All')] + [(cell['metadata__cell_line'], cell['metadata__cell_line']) for cell in Sample_Metadata.objects.values('metadata__cell_line').distinct()],
        required=False,
        label='Cell Type'
    )
    
    # Date Range fields
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False,
        label='Start Date'
    )
    
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False,
        label='End Date'
    )
    
    # Dropdown for Infection Status
    infection_status = forms.ChoiceField(
        choices=[('', 'All')] + [(infection['metadata__Infection'], infection['metadata__Infection']) for infection in Sample_Metadata.objects.values('metadata__Infection').distinct()],
        required=False,
        label='Infection Status'
    )

    def __init__(self, *args, **kwargs):
        super(SampleFilterForm, self).__init__(*args, **kwargs)
        
        # Populate Cell Type dropdown choices dynamically
        cell_type_choices = [(cell['metadata__cell_line'], cell['metadata__cell_line']) for cell in Sample_Metadata.objects.values('metadata__cell_line').distinct()]
        self.fields['cell_type'].choices = [('', 'All')] + cell_type_choices
        
        # Populate Infection Status dropdown choices dynamically
        infection_status_choices = [(infection['metadata__Infection'], infection['metadata__Infection']) for infection in Sample_Metadata.objects.values('metadata__Infection').distinct()]
        self.fields['infection_status'].choices = [('', 'All')] + infection_status_choices