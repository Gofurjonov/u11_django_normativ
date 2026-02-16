from django.db import models


class ActivePostManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()  # Matn
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)


    objects = ActivePostManager()
    all_objects = models.Manager()

    def __str__(self):
        return self.title

    def delete(self):
        self.is_deleted = True
        self.save()

    def hard_delete(self):
        super().delete()

    def restore(self):
        self.is_deleted = False
        self.save()