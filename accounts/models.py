from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings

from PIL import Image

class User(AbstractUser):
    cats = models.IntegerField(validators=[MaxValueValidator(100), MinValueValidator(1)])


class Galaxy(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(default='default_galaxy.png', upload_to='Galaxy_pics')
    followers = models.ManyToManyField('self', symmetrical=False)
    red_star_medals = models.IntegerField(default=0)  # rank 1
    gold_medals = models.IntegerField(default=0)     # top 2-10
    silver_medals = models.IntegerField(default=0)    # top 11-100
    bronze_medals = models.IntegerField(default=0)        # top 101-1000
    wood_medals = models.IntegerField(default=0)         # evryone else who posted a picture of a cat :D
    report_reason_1 = models.IntegerField(default=0)
    report_reason_2 = models.IntegerField(default=0)
    report_reason_3 = models.IntegerField(default=0)
    report_reason_4 = models.IntegerField(default=0)
    report_reason_5 = models.IntegerField(default=0)
    report_reason_6 = models.IntegerField(default=0)
    blocked = models.BooleanField(default=False)#quando esta a true , não pode dar follow, comentar, ou postar

    def __str__(self):
        return f'{self.user.username}_Galaxy'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 333 or img.width > 333:
            output_size = (333, 333)
            img.thumbnail(output_size)
            img.save(self.image.path)


class Star(models.Model): # cada kitty indivudual
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    image = models.ImageField(default='default_star.png', upload_to='Galaxy_pics')
    followers = models.ManyToManyField(Galaxy)

    def __str__(self):
        return f'{self.name}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 333 or img. width > 333:
            output_size = (333, 333)
            img.thumbnail(output_size)
            img.save(self.image.path)

