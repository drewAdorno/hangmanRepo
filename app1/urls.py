from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index),
    path('letter', views.letter),
    path('newgame/<str:difficulty>', views.newGame),
    path('addscore', views.addScore),
    path('leaderboard', views.leaderboard)
]