from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Yangi user yaratilganda profil yaratish"""
    if created:
        Profile.objects.create(user=instance)
        print(f"✅ Profil yaratildi: {instance.username}")

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """User saqlanganda profilni ham saqlash"""
    try:
        instance.profile.save()
        print(f"✅ Profil saqlandi: {instance.username}")
    except:
        print(f"❌ Profil saqlanmadi: {instance.username}")