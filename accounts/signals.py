from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import User, Galaxy, Star
from space.models import Post

@receiver(post_save, sender=User)
def create_galaxy(sender, instance, created, **kwargs):# kwargs accepts any key word argument into the end of funciton
    if created:
        Galaxy.objects.create(user=instance)

@receiver(post_save, sender=User)
def create_stars(sender, instance, created, **kwargs):
    if created:
        for cat in range(instance.cats):
            Star.objects.create(user=instance, name='cat')

@receiver(post_save, sender=User)
def save_stars(sender, instance, **kwargs): # otimizar o algoritmo depois(em termos de linhas)
    future_cats_num = instance.cats
    actual_cats_num = instance.star_set.all().count()
    if actual_cats_num<future_cats_num:
        cats_needed = future_cats_num-actual_cats_num
        for cat in range(cats_needed):
            Star.objects.create(user=instance, name='cat')

    if actual_cats_num>future_cats_num:
        cats_leftover = actual_cats_num - future_cats_num
        for cat in range(cats_leftover):
            Star.objects.last().delete()

@receiver(post_save, sender=User)
def save_galaxy(sender, instance, **kwargs):
    instance.galaxy.save()
#def save_star

