from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils import timezone
from django.conf import settings
from django.urls import reverse

from PIL import Image

from accounts.models import Galaxy, Star

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stars = models.ManyToManyField(Star)
    title = models.CharField(max_length=50)
    image = models.ImageField(upload_to='Galaxy_pics')#funcina tipo CharField Null é um ' '
    lasanhas = models.ManyToManyField(Galaxy)
    content = models.TextField(null=True) #uma tabela post id galaxy id
    reports = models.ManyToManyField(Galaxy, related_name='reports')
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if not self.content:
            img = Image.open(self.image.path)

            if img.height > 999 or img. width > 999:
                output_size = (999, 999)
                img.thumbnail(output_size)
                img.save(self.image.path)


class Comment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField(max_length=500)
    date_posted = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text

