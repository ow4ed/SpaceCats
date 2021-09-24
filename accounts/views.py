from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings


from .models import Galaxy, Star
from space.models import Post, Comment

from .forms import AccountRegisterForm, AccountUpdateForm, GalaxyUpdateForm, StarUpdateForm, \
    PostGalaxyForm, PostStarsForm, CommentForm


def register(request):

    if request.user.is_authenticated:
        context = {
            'img': '405.jpg'
        }

        return render(request, 'space/not_valid.html', context)

    if request.method == 'POST':
        form = AccountRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your galaxy has been created! You are now able to log in')#username = a_form.cleaned_data.get('username')
            return redirect('galaxy')
    else:
        form = AccountRegisterForm()

    return render(request, 'accounts/register.html', {'form': form})

@login_required
def galaxy(request):

    form = CommentForm(instance=Comment(author=request.user, ))

    posts = set()

    galaxyform = PostGalaxyForm(instance=Post(author=request.user, ))

    starform = PostStarsForm(instance=Post(author=request.user, ))
    starform.fields['stars'].queryset = request.user.star_set.all()

    for followed in Galaxy.objects.filter(followers=request.user.galaxy):
        for post in Post.objects.filter(author=followed.user):
            posts.add(post)

    for followed in Star.objects.filter(followers=request.user.galaxy):
        for post in Post.objects.all().filter(stars=followed):
            posts.add(post)

    listaDosPosts = list(posts)

    context = {
        'galaxy': request.user.galaxy,
        'show_more_info': True,
        'comment_form': form,
        'stars': Star.objects.filter(user=request.user),
        'posts': sorted(listaDosPosts, key=lambda x: x.date_posted, reverse=True),
        'galaxy_form': galaxyform,
        'stars_form': starform,
    }

    return render(request, 'accounts/galaxy.html', context)

@login_required
def my_posts(request):
    posts = set()

    for ownpost in Post.objects.filter(author=request.user):
        posts.add(ownpost)


    context = {
        'posts': sorted(posts, key=lambda x: x.date_posted, reverse=True),
        'stars': Star.objects.filter(user=request.user),
    }

    return render(request, 'accounts/myposts.html', context)

@login_required
def my_star_posts(request, star_id):

    if not Star.objects.filter(user=request.user, id=star_id):
        context = {
            'img': '404.jpg'
        }

        return render(request, 'space/not_valid.html', context)

    else:
        my_star = Star.objects.filter(user=request.user).get(id=star_id)

        posts = set()

        for post in Post.objects.all():
            if post.stars.filter(id=my_star.id):
                posts.add(post)

        context = {
            'posts': sorted(list(posts), key=lambda x: x.date_posted, reverse=True),
            'stars': Star.objects.filter(user=request.user),
            'galaxy': request.user,
            'picked_star': my_star,
        }

        return render(request, 'accounts/my_star_posts.html', context)

@login_required #não funciona
def give_lasanha(request):
    post = get_object_or_404(Post, id=request.POST.get('id'))
    is_liked = False
    if post.lasanhas.filter(user=request.user).exists():
        post.lasanhas.remove(request.user.galaxy)
        is_liked = False
    else:
        post.lasanhas.add(request.user.galaxy)
        is_liked = True

    context = {
        'post': post,
        'is_liked': is_liked,
        'total_liked': post.lasanhas.count(), # stefan onde e que tamos a usar isto ? wtf bruv
    }

    if request.is_ajax():
        html = render_to_string('space/lasanha_section.html', context, request=request)
        return JsonResponse({'form': html})


@login_required #não funciona
def follow_galaxy(request):
    galaxy = get_object_or_404(Galaxy, id=request.POST.get('id'))
    is_followed = False
    if galaxy.followers.filter(user=request.user).exists():
        galaxy.followers.remove(request.user.galaxy)
        is_followed = False
    else:
        galaxy.followers.add(request.user.galaxy)
        is_followed = True

    context = {
        'galaxy': galaxy,
        'is_followed': is_followed,
    }

    if request.is_ajax():
        html = render_to_string('space/follow_galaxy_section.html', context, request=request)
        return JsonResponse({'form': html})

@login_required #não funciona
def follow_star(request):
    star = get_object_or_404(Star, id=request.POST.get('id'))
    is_followed = False
    if star.followers.filter(user=request.user).exists():
        star.followers.remove(request.user.galaxy)
        is_followed = False
    else:
        star.followers.add(request.user.galaxy)
        is_followed = True

    context = {
        'star': star,
        'is_followed': is_followed,
        'total_followed': star.followers.count(),
    }

    if request.is_ajax():
        html = render_to_string('space/follow_star_section.html', context, request=request)
        return JsonResponse({'form': html})

@login_required
def comment(request, post_id):
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=Comment(author=request.user, post=Post.objects.get(pk=post_id), ))
        if form.is_valid():
            form.save()

        context = {
            'post': Post.objects.get(pk=post_id)
        }
        if request.is_ajax():
            html = render_to_string('space/comment_section.html', context, request=request)
            return JsonResponse({'form': html})

    context = {
        'img': '405.jpg'
    }

    return render(request, 'space/not_valid.html', context)

@login_required
def galaxy_form(request):
    if request.method == 'POST':
        form = PostGalaxyForm(request.POST, instance=Post(author=request.user,))
        if form.is_valid():
            form.save()
            return redirect('myposts')

    context = {
        'img': '405.jpg'
    }

    return render(request, 'space/not_valid.html', context)

@login_required
def stars_form(request):#################################################################################################NOT DEFAUT
    if request.method == 'POST':
        form = PostStarsForm(request.POST, request.FILES, instance=Post(author=request.user,))
        form.fields['stars'].queryset = request.user.star_set.all()
        if form.is_valid():
            form.save()
            return redirect('myposts')

    context = {
        'img': '405.jpg'
    }

    return render(request, 'space/not_valid.html', context)

@login_required
def report(request, post_id):

    post = get_object_or_404(Post, id=post_id)

    reported = 0

    if post.lasanhas.filter(user=request.user).exists():
        reported = 1

    if request.method == 'POST' and reported == 0:
        post.reports.add(request.user.galaxy)

        post_galaxy = Galaxy.objects.get(user=post.author)

        limit = Post.objects.filter(author=post_galaxy.user).count()+9

        blocked = 0

        if request.POST.get('reason1') == 'on':
            post_galaxy.report_reason_1 += 1
            post_galaxy.save()
            if post_galaxy.report_reason_1 >= limit and not post_galaxy.blocked:
                    blocked = 1
                    post_galaxy.blocked = True
                    post_galaxy.save()

        if request.POST.get('reason2') == 'on':
            post_galaxy.report_reason_2 += 1
            post_galaxy.save()
            if post_galaxy.report_reason_2 >= limit and not post_galaxy.blocked:
                    blocked = 1
                    post_galaxy.blocked = True
                    post_galaxy.save()

        if request.POST.get('reason3') == 'on':
            post_galaxy.report_reason_3 += 1
            post_galaxy.save()
            if post_galaxy.report_reason_3 >= limit and not post_galaxy.blocked:
                    blocked = 1
                    post_galaxy.blocked = True
                    post_galaxy.save()

        if request.POST.get('reason4') == 'on':
            post_galaxy.report_reason_4 += 1
            post_galaxy.save()
            if post_galaxy.report_reason_4 >= limit and not post_galaxy.blocked:
                    blocked = 1
                    post_galaxy.blocked = True
                    post_galaxy.save()
        if request.POST.get('reason5') == 'on':
            post_galaxy.report_reason_5 += 1
            post_galaxy.save()
            if post_galaxy.report_reason_5 >= limit and not post_galaxy.blocked:
                    blocked = 1
                    post_galaxy.blocked = True
                    post_galaxy.save()

        if request.POST.get('reason6') == 'on':
            post_galaxy.report_reason_6 += 1
            post_galaxy.save()
            if post_galaxy.report_reason_6 >= limit and not post_galaxy.blocked:
                    blocked = 1
                    post_galaxy.blocked = True
                    post_galaxy.save()

        if blocked == 1:
            message = 'Hello there ,unfortunately due to your recent behavior we had to block your account. ' \
                      'As soon as possible we will analyze your situation and inform you in detail of what happened. ' \
                      'Please, do not panic!'

            send_mail('Oopsie Woopsie! Uwu your galaxy got blocked',
                      message,
                      settings.EMAIL_HOST_USER,
                      [post_galaxy.user.email],)

    context = {
        'post': post,
    }

    if request.is_ajax():
        html = render_to_string('space/report_section_confirmation.html', context, request=request)
        return JsonResponse({'form': html})

    context = {
        'img': '405.jpg'
    }

    return render(request, 'space/not_valid.html', context)

@login_required
def galaxy_settings(request):
    if request.method == 'POST':
        a_form = AccountUpdateForm(request.POST, instance=request.user)
        g_form = GalaxyUpdateForm(request.POST, request.FILES, instance=request.user.galaxy)

        if a_form.is_valid() and g_form.is_valid():
            a_form.save()
            g_form.save()
            return redirect('galaxy')
    else:
        a_form = AccountUpdateForm(instance=request.user)
        g_form = GalaxyUpdateForm(instance=request.user.galaxy)

    context = {
        'a_form': a_form,
        'g_form': g_form,
    }

    return render(request, 'accounts/galaxy_settings.html', context)

@login_required
def star_settings(request, star_id):

    if not request.user.star_set.all().filter(id=star_id):

        context = {
            'img': '403.jpg'
        }

        return render(request, 'space/not_valid.html', context)

    else:
        image = request.user.star_set.all().get(id=star_id).image.url
        if request.method == 'POST':
            form = StarUpdateForm(request.POST, request.FILES, instance=request.user.star_set.all().get(id=star_id))

            if form.is_valid():
                form.save()
                return redirect('galaxy')
        else:
            form = StarUpdateForm(instance=request.user.star_set.all().get(id=star_id))

        context = {
            'form': form,
            'image': image
        }

        return render(request, 'accounts/star_settings.html', context)

@login_required
def edit_post(request, post_id):

    if not Post.objects.filter(id=post_id, author=request.user):

        context = {
            'img': '403.jpg'
        }

        return render(request, 'space/not_valid.html', context)
    else:

        post = Post.objects.get(id=post_id)

        if post.content is None:
            context = {
                'img': '405.jpg'
            }

            return render(request, 'space/not_valid.html', context)


        if request.method == 'POST':
            form = PostGalaxyForm(request.POST, instance=post)
            if form.is_valid():
                form.save()
                return redirect('myposts')

        else:
            form = PostGalaxyForm(instance=post)

        context = {
            'form': form,
            'post': post,
        }

        return render(request, 'accounts/edit_post.html', context)

