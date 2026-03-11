from django.core.mail import send_mail
from django.conf import settings
import threading


def send_email_thread(subject, message, recipient_list):
    """Email yuborish (thread orqali)"""

    def send():
        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=recipient_list,
                fail_silently=False,
            )
            print(f"Email yuborildi: {recipient_list}")
        except Exception as e:
            print(f"Email yuborishda xatolik: {e}")

    thread = threading.Thread(target=send)
    thread.start()
    return thread