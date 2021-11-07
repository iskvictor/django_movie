from django.shortcuts import render, redirect
from django.views.generic.base import View
from .models import Movie, Category
from django.views.generic import ListView, DetailView
from .forms import ReviewForm


class MoviesView(ListView):
    """ Список фильмов """
    model = Movie
    queryset = Movie.objects.filter(draft=False)
    

class MovieDetailView(DetailView):

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