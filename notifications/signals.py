from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from posts.models import Post
from .models import Notification

@receiver(post_save, sender=Post)
def new_post_notification(sender, instance, created, **kwargs):
    if created:
        users = User.objects.exclude(id=instance.user.id)
        for user in users:
            Notification.objects.create(
                user=user,
                message=f"Yangi post: {instance.title[:30]}"
            )