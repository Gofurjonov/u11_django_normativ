from django.db import models
from django.contrib.auth.models import User


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