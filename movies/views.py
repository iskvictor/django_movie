from django.shortcuts import render, redirect
from django.views.generic.base import View
from .models import Actor, Movie, Category, Genre
from django.views.generic import ListView, DetailView
from .forms import ReviewForm
from django.db.models import Q 

class GenreYear:
    """Жанры и года выхода фильмов"""
    def get_genres(self):
        return Genre.objects.all()

    def get_years(self):
        return Movie.objects.filter(draft=False).values("year")


class MoviesView(GenreYear, ListView):
    """ Список фильмов """
    model = Movie
    queryset = Movie.objects.filter(draft=False)
    

class MovieDetailView(GenreYear, DetailView):

    model = Movie
    slug_field = "url"


class AddReview(View):
    "Отзывы"
    def post(self, request, pk):
        form = ReviewForm(request.POST)
        movie = Movie.objects.get(id=pk)
        if form.is_valid():
            new_review = form.save(commit=False)
            if request.POST.get('parent', None):
                new_review.parent_id = int(request.POST.get('parent'))
            new_review.movie = movie
            new_review.save()
        return redirect(movie.get_absolute_url())


class ActorView(GenreYear, DetailView):
    """Вывод информации о актере"""
    model = Actor
    template_name = "movies/actor.html"
    slug_field = "name"


class FilterMoviesView(GenreYear, ListView):
    def get_queryset(self):
        queryset = Movie.objects.filter(
            Q(year__in=self.request.GET.getlist('year')) |
            Q(genres__in = self.request.GET.getlist('genre'))
            )
        return queryset