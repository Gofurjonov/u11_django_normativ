from django.db import models

from django.contrib.auth.models import User


class Document(models.Model):
    title = models.CharField(max_length=200, verbose_name="Fayl nomi")
    file = models.FileField(upload_to='documents/', verbose_name="Fayl")
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Yuklagan foydalanuvchi")
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="Yuklangan vaqt")

    objects = models.Manager()

    class Meta:
        verbose_name = "Hujjat"
        verbose_name_plural = "Hujjatlar"
        ordering = ['-uploaded_at']

    def __str__(self):
        return self.title

    def filename(self):
        return self.file.name.split('/')[-1]