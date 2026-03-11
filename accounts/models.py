import random
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta


class Profile(models.Model):
    # Foydalanuvchi profili - avatar uchun
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name="Profil rasmi")
    bio = models.TextField(blank=True, null=True, verbose_name="Bio")

    def __str__(self):
        return f"{self.user.username} profili"

    class Meta:
        verbose_name = "Profil"
        verbose_name_plural = "Profillar"


class PasswordResetCode(models.Model):
    """Parol tiklash uchun verification code"""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reset_codes')
    code = models.CharField(max_length=6, verbose_name="Tasdiqlash kodi")
    created_at = models.DateTimeField(auto_now_add=True)
    expired_at = models.DateTimeField(verbose_name="Amal qilish muddati")
    is_used = models.BooleanField(default=False, verbose_name="Ishlatilganmi?")

    class Meta:
        verbose_name = "Parol tiklash kodi"
        verbose_name_plural = "Parol tiklash kodlari"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.code}"

    @staticmethod
    def generate_code():
        """6 xonali random code yaratish"""
        return str(random.randint(100000, 999999))

    @staticmethod
    def get_expired_date():
        """Code amal qilish muddati (2 daqiqa)"""
        return timezone.now() + timedelta(minutes=2)

    def is_valid(self):
        """Code hali amal qiladimi?"""
        return not self.is_used and self.expired_at > timezone.now()