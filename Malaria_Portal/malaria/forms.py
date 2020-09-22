from django import forms

from .models import Patient

class PatientForm(forms.ModelForm):
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    class Meta:
        model = Patient
        fields = ('full_name', 'gender', 'date_of_birth')