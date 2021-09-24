from django.shortcuts import render, get_object_or_404

import datetime

from .models import Post, Comment
from accounts.models import User, Galaxy, Star

from accounts.forms import CommentForm

def order_list_by_lasanhas(lista):

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

    return lista

def home(request):
    posts = set()

    form = None

    if User.objects.filter(id=request.user.id).count() > 0:
        form = CommentForm(instance=Comment(author=request.user, ))

    for stars in Star.objects.all():
        for post in Post.objects.all().filter(stars=stars):
            posts.add(post)

    starPosts = order_list_by_lasanhas(list(posts))[:6] #eficencia x600

    context = {
        'comment_form': form,
        'posts': Post.objects.all().order_by('-date_posted'),
        "ranking": starPosts,
    }

    return render(request, 'space/home.html', context)


def galaxys_galaxy(request, username):

    if not User.objects.filter(username=username):
        context = {
            'img': '404.jpg'
        }

        return render(request, 'space/not_valid.html', context)

    else:

        form = None

        if User.objects.filter(id=request.user.id).count() > 0:
            form = CommentForm(instance=Comment(author=request.user, ))

        user = User.objects.get(username=username)

        posts = Post.objects.filter(author=user.id).count() #o id e mais rapido ?

        followers = set()

        for follower in user.galaxy.followers.all():

            followers.add(follower)

        lasanhas = 0
        for post in Post.objects.filter(author=user.id):
            if post.content is None:
                lasanhas+=post.lasanhas.count()

        context = {
            'comment_form': form,
            'galaxy': user.galaxy,
            'total_posts': posts,
            'total_lasanhas':lasanhas, #total de somados na galaxia
            'stars': Star.objects.filter(user=user.id),
            'posts': Post.objects.filter(author=user.id).order_by('-date_posted'),
            'followers': followers,
            'show_more_info': True,
        }

        return render(request, 'space/galaxys_galaxy.html', context)

def search(request):

    if request.method == 'POST':

        search = request.POST['search']

        users = User.objects.filter(username=search)
        if not users:
            stars = Star.objects.filter(name=search)

            posts = set()

            for post in Post.objects.all():
                if post.stars.filter(name=search).count() != 0 or post.title == search:
                    posts.add(post)

            if not stars and not posts: ## não encontrou users nem estrelas
                search = " FAC! nothing found"
                context = {
                    'search': search
                }
                return render(request, 'space/search.html', context)

            galaxys = set()
            for user in users:
                galaxys.add(user.galaxy)
            for star in stars:
                galaxys.add(star.user.galaxy)

            context = {
                'galaxys': galaxys,
                'posts': posts,

            }

            return render(request, 'space/search.html', context)

        else:
            galaxys = set()
            for user in users:
                galaxys.add(user.galaxy)

            context = {
                'galaxys': galaxys,
            }

            return render(request, 'space/search.html', context)
    else:
        context = {
            'img': '405.jpg'
        }

        return render(request, 'space/not_valid.html', context)

def ladder_ranking(request):

    galaxys = Galaxy.objects.all().order_by('-red_star_medals', '-gold_medals', '-silver_medals', '-bronze_medals',
                                            '-wood_medals')

    context = {
        'galaxys': galaxys
    }

    return render(request, 'space/ladder_ranking.html', context)


def hall_of_fame(request):
    posts_current_month = \
        Post.objects.filter(content=None, date_posted__year=datetime.datetime.now().year,
                            date_posted__month=datetime.datetime.now().month).order_by('-date_posted')
    #o date posted = pela logica se 2 posts tem o mesmo numero de lasanhas , e um for postato mais recentemente, esse
    # postado mais recentemente é o melhor para a audiencia
    posts = order_list_by_lasanhas(list(posts_current_month))

    context = {
        'posts': posts
    }

    return render(request, 'space/hall_of_fame.html', context)

def hall_of_fame_last_month(request):
    posts_last_month = \
        Post.objects.filter(content=None, date_posted__year=datetime.datetime.now().year,
                            date_posted__month=datetime.datetime.now().month-1).order_by('-date_posted')

    posts = order_list_by_lasanhas(list(posts_last_month))

    context = {
        'posts': posts
    }

    return render(request, 'space/hall_of_fame.html', context)

def about(request):
    return render(request, 'space/about.html', {'title': 'About'})


