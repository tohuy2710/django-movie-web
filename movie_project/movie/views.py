from django.shortcuts import render, get_object_or_404
from .models import Movielink, Movieinfo, Usercomment
from django.db.models import Subquery, Avg

def filmplayer(request, id, ep : str):
    movie = get_object_or_404(Movieinfo, movieid=id)
    movieEpList = Movielink.objects.filter(movieid=id)
    movieEp = get_object_or_404(Movielink, movieid=id, episode=ep)
    context = {
        'movieEp': movieEp,
        'movie': movie,
        'movieEpList': movieEpList
    }
    print(movie.name)
    return render(request, 'filmplayer.html', context)

def filminfo(request, id):
    movie = get_object_or_404(Movieinfo, movieid=id)
    movieEpList = Movielink.objects.filter(movieid=id)
    context = {
        'movie': movie,
        'movieEpList': movieEpList
    }
    return render(request, 'filminfo.html', context)

def home(request):
    recentlyUpdateMovie = Movieinfo.objects.all().order_by('-lastupdatedate')[:18]
    top_movies = (
        Usercomment.objects
        .values("movieid")
        .annotate(avg_star=Avg("star"))
        .order_by("-avg_star")
        .values("movieid")[0:5]
    )

    topRateMovies = Movieinfo.objects.filter(movieid__in=[movie['movieid'] for movie in top_movies])

    context = {
        'ruMovie': recentlyUpdateMovie,
        'trMovie': topRateMovies
    }
    return render(request, 'home.html', context)


#name, status. duration, type, publishYar, lang, genre, nation, thuming, coverimg, reuiredage, content