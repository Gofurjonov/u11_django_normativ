from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from .forms import RegisterForm, LoginForm
from django.contrib.auth.decorators import login_required
from .models import Profile
from .forms import ProfileForm
from django.contrib.auth.models import Group
from .common.email import send_password_reset_email, send_welcome_email
from django.utils.translation import gettext as _


def my_view(request):
    title = _("Bosh sahifa")
    message = _("Xush kelibsiz!")

    context = {
        'title': title,
        'message': message,
    }
    return render(request, 'index.html', context)

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()

            user_group = Group.objects.get(name='User')
            user.groups.add(user_group)

            #  Xush kelibsiz emaili yuborish
            send_welcome_email(user)

            messages.success(request, f"{user.username} muvaffaqiyatli ro'yxatdan o'tdi!")
            return redirect('accounts:login')
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            login(request, user)
            messages.success(request, f"Xush kelibsiz, {user.username}!")
            return redirect('post_list')
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('/accounts/login/')


@login_required
def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    return render(request, 'accounts/profile.html', {'profile': profile})


@login_required
def edit_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profil muvaffaqiyatli yangilandi!")
            return redirect('accounts:profile')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'accounts/edit_profile.html', {'form': form})


# 🆕 Forgot Password
def forgot_password(request):
    """Parolni tiklash - username kiritish va code yuborish"""
    from django.contrib.auth.models import User
    from .models import PasswordResetCode

    if request.method == 'POST':
        from .forms import ForgotPasswordForm
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            user = User.objects.get(username=username)

            # Eski kodlarni bekor qilish
            PasswordResetCode.objects.filter(user=user, is_used=False).update(is_used=True)

            # Yangi code yaratish
            code = PasswordResetCode.objects.create(
                user=user,
                code=PasswordResetCode.generate_code(),
                expired_at=PasswordResetCode.get_expired_date()
            )

            # 📧 Email yuborish
            send_password_reset_email(user, code.code)

            messages.success(request, f"📧 Kod {user.email} manziliga yuborildi!")
            request.session['reset_user_id'] = user.id
            return redirect('accounts:restore_password')
    else:
        from .forms import ForgotPasswordForm
        form = ForgotPasswordForm()

    return render(request, 'accounts/forgot_password.html', {'form': form})


def restore_password(request):
    """Yangi parol o'rnatish (5-qadam)"""
    from django.shortcuts import get_object_or_404
    from django.contrib.auth.models import User
    from .models import PasswordResetCode
    from .forms import RestorePasswordForm

    user_id = request.session.get('reset_user_id')
    if not user_id:
        messages.error(request, "Avval username kiriting!")
        return redirect('accounts/forgot_password.html')

    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        code = request.POST.get('code')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password != confirm_password:
            messages.error(request, "Parollar mos emas!")
            return redirect('accounts/restore_password.html')

        try:
            code_obj = PasswordResetCode.objects.filter(
                user=user,
                code=code,
                is_used=False
            ).latest('created_at')
        except PasswordResetCode.DoesNotExist:
            messages.error(request, "Kod noto'g'ri!")
            return redirect('accounts/restore_password.html')


        if not code_obj.is_valid():
            messages.error(request, "Kodning muddati tugagan! Qaytadan so'rang.")
            del request.session['reset_user_id']
            return redirect('accounts/forgot_password.html')


        user.set_password(new_password)
        user.save()


        code_obj.is_used = True
        code_obj.save()

        del request.session['reset_user_id']

        messages.success(request, "Parol muvaffaqiyatli yangilandi! Endi tizimga kirishingiz mumkin.")
        return redirect('accounts:login')

    return render(request, 'accounts/restore_password.html', {'email': user.email})