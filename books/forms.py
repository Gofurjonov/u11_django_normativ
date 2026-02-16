from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    title = forms.CharField(max_length=255, label='title')
    author = forms.CharField(max_length=255, label='author')
    price = forms.DecimalField(max_digits=10, decimal_places=2)

class BookModelForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'price', 'author']