from django import forms
from .models import Transaction

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = [
            'type', 'date', 'party_name', 
            'district', 'branch', 'crop_year',
            'godown', 'crop', 'bags', 'weight',
            # NEW FIELDS ADDED HERE
            'stack_no', 'hamar_labor', 
            'truck_number', 'gate_pass', 'shortage'
        ]
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'party_name': forms.TextInput(attrs={'class': 'form-control', 'list': 'party_list_ids'}),
            'district': forms.TextInput(attrs={'class': 'form-control'}),
            'branch': forms.TextInput(attrs={'class': 'form-control'}),
            'crop_year': forms.TextInput(attrs={'class': 'form-control'}),
            'godown': forms.Select(attrs={'class': 'form-select'}),
            'crop': forms.Select(attrs={'class': 'form-select'}),
            'bags': forms.NumberInput(attrs={'class': 'form-control'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control'}),
            'type': forms.HiddenInput(),

            # --- NEW WIDGETS ---
            'stack_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Stack No (e.g. 666)'}),
            'hamar_labor': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Labor Name'}),
            'truck_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Truck No (e.g. MP-09-AB-1234)'}),
            'gate_pass': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Gate Pass No'}),
            'shortage': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00'}),
        }

class BulkImportForm(forms.Form):
    file = forms.FileField(widget=forms.FileInput(attrs={
        'class': 'form-control form-control-lg', 
        'accept': '.xlsx, .xls, .csv'
    }))