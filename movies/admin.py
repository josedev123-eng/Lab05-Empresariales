from django.contrib import admin
from django.db.models import Avg, Count
from django.utils.html import format_html

from .models import Genre, Movie, Person, Rating


class RatingInline(admin.TabularInline):
    """Paso 6: valoraciones como bloque de líneas dentro de la película."""
    model = Rating
    extra = 1
    fields = ['reviewer_name', 'score', 'comment']
    show_change_link = True


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name', 'movie_count']
    search_fields = ['name']

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(_movie_count=Count('movies'))

    @admin.display(description='N.º películas', ordering='_movie_count')
    def movie_count(self, obj):
        return obj._movie_count


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ['thumb', 'name', 'birth_date', 'created_at']
    list_filter = ['birth_date']
    search_fields = ['name', 'biography']
    readonly_fields = ['photo_preview', 'created_at', 'updated_at']
    date_hierarchy = 'birth_date'

    @admin.display(description='Foto')
    def thumb(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="width:40px;height:40px;object-fit:cover;border-radius:50%">', obj.photo.url)
        return '—'

    @admin.display(description='Vista previa')
    def photo_preview(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="max-width:200px;border-radius:12px">', obj.photo.url)
        return 'Sin foto'


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['thumb', 'title', 'year', 'director', 'display_genres', 'avg_score', 'rating_count']
    list_filter = ['genres', 'year']
    search_fields = ['title', 'director__name', 'cast__name']
    readonly_fields = ['poster_preview', 'created_at', 'updated_at']
    filter_horizontal = ['genres', 'cast']
    autocomplete_fields = ['director']
    inlines = [RatingInline]
    date_hierarchy = 'created_at'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(_avg=Avg('ratings__score'), _count=Count('ratings')).prefetch_related('genres')

    @admin.display(description='Géneros')
    def display_genres(self, obj):
        return ', '.join(g.name for g in obj.genres.all())

    @admin.display(description='Nota media', ordering='_avg')
    def avg_score(self, obj):
        return round(obj._avg, 2) if obj._avg is not None else '—'

    @admin.display(description='Valoraciones', ordering='_count')
    def rating_count(self, obj):
        return obj._count

    @admin.display(description='Póster')
    def thumb(self, obj):
        if obj.poster:
            return format_html('<img src="{}" style="width:40px;height:60px;object-fit:cover;border-radius:6px">', obj.poster.url)
        return '—'

    @admin.display(description='Vista previa del póster')
    def poster_preview(self, obj):
        if obj.poster:
            return format_html('<img src="{}" style="max-width:220px;border-radius:12px">', obj.poster.url)
        return 'Sin póster (súbelo en el campo Poster de abajo)'


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ['movie', 'reviewer_name', 'score', 'created_at']
    list_filter = ['score', 'movie__genres', 'movie__year']
    search_fields = ['movie__title', 'reviewer_name']
    readonly_fields = ['created_at', 'updated_at']
    autocomplete_fields = ['movie']
