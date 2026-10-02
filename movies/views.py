from django.db.models import Avg, Count
from django.shortcuts import get_object_or_404, render

from .models import Genre, Movie


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
    query = request.GET.get('q', '').strip()
    genre_id = request.GET.get('genero', '')
    movies = Movie.objects.annotate(avg_score=Avg('ratings__score')).prefetch_related('genres')
    if query:
        movies = movies.filter(title__icontains=query)
    active_genre = None
    if genre_id.isdigit():
        active_genre = Genre.objects.filter(pk=int(genre_id)).first()
        if active_genre:
            movies = movies.filter(genres=active_genre)
    movies = movies.order_by('-avg_score', '-year', 'title')
    genres = Genre.objects.annotate(n=Count('movies')).filter(n__gt=0).order_by('name')
    return render(request, 'movies/movie_list.html', {
        'movies': movies,
        'genres': genres,
        'query': query,
        'active_genre': active_genre,
    })


def movie_detail(request, pk):
    movie = get_object_or_404(
        Movie.objects.prefetch_related('genres', 'cast', 'ratings').select_related('director'),
        pk=pk,
    )
    ratings = list(movie.ratings.all())
    total = len(ratings)
    dist = {s: 0 for s in range(1, 6)}
    for r in ratings:
        dist[r.score] = dist.get(r.score, 0) + 1
    bars = [{'stars': s, 'count': dist[s],
             'pct': round(dist[s] * 100 / total) if total else 0} for s in range(5, 0, -1)]
    recommendations = get_recommendations(movie, limit=5)
    return render(
        request,
        'movies/movie_detail.html',
        {'movie': movie, 'recommendations': recommendations,
         'rating_bars': bars, 'rating_total': total},
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
