from django.db.models import Avg
from django.shortcuts import get_object_or_404, render

from .models import Movie


def get_recommendations(movie, limit=5):
    """Películas del mismo género mejor valoradas (excluye la propia)."""
    genre_ids = movie.genres.values_list('id', flat=True)
    if not genre_ids:
        return Movie.objects.none()
    return (
        Movie.objects.filter(genres__in=genre_ids)
        .exclude(pk=movie.pk)
        .annotate(avg_score=Avg('ratings__score'))
        .order_by('-avg_score', '-year', 'title')
        .distinct()[:limit]
    )


def movie_list(request):
    movies = Movie.objects.annotate(avg_score=Avg('ratings__score')).prefetch_related('genres')
    return render(request, 'movies/movie_list.html', {'movies': movies})


def movie_detail(request, pk):
    movie = get_object_or_404(
        Movie.objects.prefetch_related('genres', 'cast').select_related('director'),
        pk=pk,
    )
    recommendations = get_recommendations(movie, limit=5)
    return render(
        request,
        'movies/movie_detail.html',
        {'movie': movie, 'recommendations': recommendations},
    )


def movie_recommendations(request, pk):
    """Vista pública exigida por el laboratorio (paso 10)."""
    movie = get_object_or_404(Movie, pk=pk)
    recommendations = get_recommendations(movie, limit=5)
    return render(
        request,
        'movies/movie_recommendations.html',
        {'movie': movie, 'recommendations': recommendations},
    )
