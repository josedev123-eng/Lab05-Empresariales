from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Avg


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'género'
        verbose_name_plural = 'géneros'

    def __str__(self):
        return self.name


class Person(models.Model):
    name = models.CharField(max_length=200)
    birth_date = models.DateField(null=True, blank=True)
    biography = models.TextField(blank=True)
    photo = models.ImageField(upload_to='persons/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'persona'
        verbose_name_plural = 'personas'

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=200, db_index=True)
    year = models.PositiveIntegerField(db_index=True)
    synopsis = models.TextField(blank=True)
    duration_minutes = models.PositiveIntegerField(null=True, blank=True)
    poster = models.ImageField(upload_to='posters/', blank=True, null=True)
    genres = models.ManyToManyField(Genre, related_name='movies', blank=True)
    director = models.ForeignKey(
        Person,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='directed_movies',
    )
    cast = models.ManyToManyField(Person, related_name='acted_movies', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-year', 'title']
        verbose_name = 'película'
        verbose_name_plural = 'películas'

    def __str__(self):
        return f'{self.title} ({self.year})'

    @property
    def avg_rating(self):
        result = self.ratings.aggregate(avg=Avg('score'))['avg']
        return round(result, 2) if result is not None else None

    def genre_list(self):
        return ', '.join(g.name for g in self.genres.all())
    genre_list.short_description = 'Géneros'


class Rating(models.Model):
    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        related_name='ratings',
    )
    reviewer_name = models.CharField(max_length=100)
    score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-score', '-created_at']
        verbose_name = 'valoración'
        verbose_name_plural = 'valoraciones'

    def __str__(self):
        return f'{self.movie.title} — {self.score}/5 por {self.reviewer_name}'
