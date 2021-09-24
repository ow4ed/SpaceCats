from django_cron import CronJobBase, Schedule
import datetime

from .models import Post
from accounts.models import Galaxy

class MyCronJob(CronJobBase):
    RUN_EVERY_MINS = 43193# nearly every 1 september month, because developers are born in september

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'accounts.my_cron_job'    # a unique code

    def do(self):

        posts_current_month = Post.objects.filter(content=None,
                                                  date_posted__year=datetime.datetime.now().year,
                                                  date_posted__month=datetime.datetime.now().month)

        lista = list(posts_current_month)

        n = len(lista)

        # Traverse through all array elements
        for i in range(n):
            # Last i elements are already in place
            for j in range(0, n - i - 1):
                # traverse the array from 0 to n-i-1
                # Swap if the element found is greater
                # than the next element
                if lista[j].lasanhas.count() < lista[j + 1].lasanhas.count():
                    lista[j], lista[j + 1] = lista[j + 1], lista[j]

        lista[0].author.galaxy.red_star_medals += 1
        lista[0].author.galaxy.save()

        for post in lista[1:11]:
            post.author.galaxy.gold_medals += 1
            post.author.galaxy.save()

        for post in lista[11:101]:
            post.author.galaxy.silver_medals += 1
            post.author.galaxy.save()

        for post in lista[101:1001]:
            post.author.galaxy.bronze_medal += 1
            post.author.galaxy.save()

        for post in lista[1001:]:
            post.author.galaxy.wood_medal += 1
            post.author.galaxy.save()


