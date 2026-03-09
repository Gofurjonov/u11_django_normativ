from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'image']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Post sarlavhasi'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Post matni',
                'rows': 5
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            })
        }
        labels = {
            'title': 'Sarlavha',
            'content': 'Matn',
            'image': 'Rasm yuklash'
        }