import datetime
import os
from django.http import HttpResponseForbidden
from django.conf import settings


class UserAgentLogger:

    def __init__(self, get_response):
        self.get_response = get_response
        self.log_file = os.path.join(settings.BASE_DIR, 'requests.log')
        print(f"📁 Log fayl manzili: {self.log_file}")

    def __call__(self, request):
        # Har bir so'rovda ishlaydi
        user_agent = request.META.get('HTTP_USER_AGENT', 'Noma\'lum')
        print(f"\n Brauzer: {user_agent[:50]}...")

        response = self.get_response(request)
        return response


class TimeRestriction:
    """Faqat 08:00 - 18:00 oralig'ida ishlaydi"""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Hozirgi soat
        soat = datetime.datetime.now().hour

        # Admin panelga cheklov yo'q
        if request.path.startswith('/admin/'):
            return self.get_response(request)

        # Soat 8 dan 18 gacha?
        if soat < 8 or soat >= 21:
            return HttpResponseForbidden("""
                <h1>⏰ Vaqt chegarasi</h1>
                <p>Sayt 08:00 dan 18:00 gacha ishlaydi!</p>
                <p>Hozir: <strong>{}:00</strong></p>
            """.format(soat))

        return self.get_response(request)


class RequestLoggerMiddleware:
    """
    Har bir requestni log faylga yozadi
    """

    def __init__(self, get_response):
        self.get_response = get_response
        # Log fayl nomi
        self.log_file = 'requests.log'

        # Fayl boshiga sarlavha yozish (agar fayl yangi bo'lsa)
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w', encoding='utf-8') as f:
                f.write("=== REQUEST LOG ===\n")
                f.write("Vaqt | Foydalanuvchi | IP | URL | Method\n")
                f.write("-" * 70 + "\n")

    def __call__(self, request):
        # 1. Vaqt
        now = datetime.datetime.now()
        vaqt = now.strftime("%Y-%m-%d %H:%M:%S")

        # 2. Foydalanuvchi
        if hasattr(request, 'user') and request.user.is_authenticated:
            user = request.user.username
        else:
            user = "AnonymousUser"

        # 3. IP manzil
        ip = request.META.get('REMOTE_ADDR', '0.0.0.0')

        # 4. URL va Method
        method = request.method
        path = request.path

        # Log yozuvi
        log_entry = f"{vaqt} | {user} | {ip} | {method} {path}\n"

        # Faylga yozish
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(log_entry)
        except Exception as e:
            print(f"Log yozishda xatolik: {e}")

        # Requestni davom ettirish
        response = self.get_response(request)
        return response