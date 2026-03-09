from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Post
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Post)
def post_created_signal(sender, instance, created, **kwargs):
    """Post yaratilganda yoki o'zgartirilganda ishlaydi"""
    action = "yaratildi" if created else "yangilandi"
    print(f"📝 Post {action}: {instance.title}")
    print(f"   Muallif: {instance.user.username if hasattr(instance, 'user') else 'Noma\'lum'}")
    print(f"   Vaqt: {instance.created_at}")
    logger.info(f"Post {action}: {instance.title}")

@receiver(post_delete, sender=Post)
def post_deleted_signal(sender, instance, **kwargs):
    """Post o'chirilganda ishlaydi"""
    print(f"🗑️ Post o'chirildi: {instance.title}")
    logger.info(f"Post o'chirildi: {instance.title}")