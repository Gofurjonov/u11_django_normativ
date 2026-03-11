import threading
from django.core.mail import send_mail
from django.conf import settings


def send_email_thread(subject, message, recipient_list):
    """Email yuborish (thread bilan)"""

    def send():
        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=recipient_list,
                fail_silently=False,
            )
            print(f" Email yuborildi: {recipient_list}")
        except Exception as e:
            print(f" Xatolik: {e}")

    threading.Thread(target=send).start()


def send_password_reset_email(user, code):
    """Parol tiklash kodi yuborish"""
    subject = f"Parolni tiklash kodi - {user.username}"
    message = f"""
    Salom {user.username}!

    Parolni tiklash kodingiz: {code}

    Kod 2 daqiqa amal qiladi.

    MyBlog
    """
    send_email_thread(subject, message, [user.email])


def send_welcome_email(user):
    """Xush kelibsiz emaili"""
    subject = f"Xush kelibsiz, {user.username}!"
    message = f"""
    {user.username}, MyBlog'ga xush kelibsiz!

    Profilingizni to'ldirishni unutmang.

    MyBlog
    """
    send_email_thread(subject, message, [user.email])