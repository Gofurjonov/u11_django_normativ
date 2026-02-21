from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate


class RegisterForm(forms.ModelForm):

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Parol'
        }),
        label='Parol'
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Parolni tasdiqlang'
        }),
        label='Parolni tasdiqlang'
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password']  # Qaysi maydonlar ishlatiladi
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Username'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email'
            }),
        }
        labels = {
            'username': 'Foydalanuvchi nomi',
            'email': 'Email',
        }

    def clean_username(self):
        """Username unique ekanligini tekshirish"""
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("Bu username allaqachon mavjud!")
        return username

    def clean_email(self):
        """Email unique ekanligini tekshirish"""
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            raise ValidationError("Bu email allaqachon mavjud!")
        return email

    def clean(self):
        """Password va confirm_password tengligini tekshirish"""
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise ValidationError("Parollar bir-biriga mos kelmadi!")

        return cleaned_data

    def save(self, commit=True):
        """User yaratish va parolni hashlash"""
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])  # MUHIM: parolni hashlash

        if commit:
            user.save()

        return user


class LoginForm(forms.Form):
    """Custom login form - authenticate bilan"""

    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username'
        }),
        label='Foydalanuvchi nomi'
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Parol'
        }),
        label='Parol'
    )

    def clean(self):
        """Authenticate orqali userni tekshirish"""
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)

            if not user:
                raise ValidationError("Username yoki parol noto'g'ri!")

            # Userni cleaned_data ga qo'shamiz (view da ishlatish uchun)
            cleaned_data['user'] = user

        return cleaned_data