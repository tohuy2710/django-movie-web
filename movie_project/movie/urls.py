from django.urls import path
from . import views

urlpatterns = [
    path('filmplayer/<int:id>/', views.filminfo, name='filminfo'),
    path('filmplayer/<int:id>/<str:ep>/', views.filmplayer, name='filmplayer'),
    path('home/', views.home, name='home'),
]
