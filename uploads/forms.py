from django import forms
from .models import Document

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['title', 'file']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Fayl nomi'}),
            'file': forms.FileInput(attrs={'class': 'form-control'})
        }
        labels = {
            'title': 'Fayl nomi',
            'file': 'Fayl'
        }