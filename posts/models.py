from django.db import models
from django.contrib.auth.models import User


class ActivePostManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name="Sarlavha")
    content = models.TextField(verbose_name="Matn")

    image = models.ImageField(
        upload_to='posts/',
        null=True,
        blank=True,
        verbose_name="Rasm"
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Yangilangan")
    is_deleted = models.BooleanField(default=False, verbose_name="O'chirilganmi?")

    # Agar user field kerak bo'lsa
    # user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    objects = ActivePostManager()
    all_objects = models.Manager()

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Postlar"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def delete(self):
        self.is_deleted = True
        self.save()

    def hard_delete(self):
        if self.image:
            self.image.delete()
        super().delete()

    def restore(self):
        self.is_deleted = False
        self.save()