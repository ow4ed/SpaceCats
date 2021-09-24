from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='space-home'),
    path('about/', views.about, name='space-about'),
    path('ladder-ranking/', views.ladder_ranking, name='ladder_ranking'),
    path('hall-of-fame/', views.hall_of_fame, name='space_hall_of_fame'),
    path('space-hall-of-fame-last-month/', views.hall_of_fame_last_month, name='space_hall_of_fame_last_month'),
    # where do i put this ?
    path('galaxys/<str:username>', views.galaxys_galaxy, name='galaxys_galaxy'),
    path('search/', views.search, name='search'),

]

