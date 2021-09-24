"""SpaceCats URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from accounts import views as accounts_views

from django.conf.urls import url

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', accounts_views.register, name='register'),
    path('galaxy/', accounts_views.galaxy, name='galaxy'),
    path('give-lasanha/', accounts_views.give_lasanha, name='give_lasanha'),
    path('follow-galaxy/', accounts_views.follow_galaxy, name='follow_galaxy'),
    path('follow-star/', accounts_views.follow_star, name='follow_star'),
    path('comment/<int:post_id>', accounts_views.comment, name='comment'),
    path('galaxy-post/', accounts_views.galaxy_form, name='galaxy_form'),
    path('stars-post/', accounts_views.stars_form, name='stars_form'),
    path('myPosts/', accounts_views.my_posts, name='myposts'),
    path('myStarPosts/<int:star_id>', accounts_views.my_star_posts, name='my_star_posts'),
    path('edit-post/<int:post_id>', accounts_views.edit_post, name='edit_post'),
    path('report/<int:post_id>', accounts_views.report, name='report'),
    path('galaxy-settings/', accounts_views.galaxy_settings, name='galaxy_settings'),
    path('star-settings/<int:star_id>', accounts_views.star_settings, name='star_settings'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='accounts/logout.html'), name='logout'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'),name='password_reset_complete'),
    path('', include('space.urls')),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
