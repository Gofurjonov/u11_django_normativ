from django.contrib import messages
from django.shortcuts import render, redirect
from django.core.exceptions import PermissionDenied

def login_required(func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, "Iltimos, avval tizimga kiring!")
            return redirect('accounts:login')
        return func(request, *args, **kwargs)
    return wrapper

