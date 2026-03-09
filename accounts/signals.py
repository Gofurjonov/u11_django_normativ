from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
import logging
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


logger = logging.getLogger(__name__)

@receiver(post_save, sender=User)
def user_created_signal(sender, instance, created, **kwargs):
    """
    User yaratilganda ishlaydigan signal
    """
    if created:
        # 1. Console ga log chiqarish
        print(f"✅ YANGI USER YARATILDI: {instance.username} (ID: {instance.id})")
        print(f"   Email: {instance.email}")
        print(f"   Vaqt: {instance.date_joined}")

        # 2. Log faylga yozish
        logger.info(f"Yangi user yaratildi: {instance.username}")

        # 3. Profil yaratish (agar avtomatik yaratilmasa)
        from .models import Profile
        Profile.objects.get_or_create(user=instance)

        # 4. User group ga qo'shish (agar kerak bo'lsa)
        from django.contrib.auth.models import Group
        user_group, _ = Group.objects.get_or_create(name='User')
        instance.groups.add(user_group)

        print(f"   ✅ User group ga qo'shildi: User")
        print("-" * 50)


@receiver(post_save, sender=User)
def user_login_signal(sender, instance, **kwargs):
    """
    User har safar saqlanganda ishlaydi
    """
    print(f"👤 User ma'lumotlari yangilandi: {instance.username}")