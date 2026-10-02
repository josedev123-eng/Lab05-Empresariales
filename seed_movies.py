"""Seed del laboratorio Admin con Django: app movies.
Idempotente: puede ejecutarse varias veces sin duplicar.

Crea:
- superusuario admin / admin123
- 4 géneros, personas, 10 películas
- valoraciones en 6 películas
- grupo «editores» (add + change movie, sin delete) + usuario editor / editor123
"""
import os

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import Group, Permission, User  # noqa: E402
from movies.models import Genre, Movie, Person, Rating  # noqa: E402

# 1. Superusuario
admin, _ = User.objects.get_or_create(
    username='admin',
    defaults={'email': 'admin@example.com', 'is_staff': True, 'is_superuser': True},
)
admin.set_password('admin123')
admin.is_staff = True
admin.is_superuser = True
admin.email = 'admin@example.com'
admin.save()

# 2. Géneros (4)
genres_data = {
    'Drama': 'Conflictos humanos y emocionales.',
    'Comedia': 'Humor y situaciones ligeras.',
    'Ciencia ficción': 'Futuro, espacio y tecnología.',
    'Terror': 'Suspense y miedo.',
}
genres = {}
for name, desc in genres_data.items():
    g, _ = Genre.objects.get_or_create(name=name, defaults={'description': desc})
    genres[name] = g

# 3. Personas (directores / reparto)
people_data = [
    ('Denis Villeneuve', '1967-10-03'),
    ('Christopher Nolan', '1970-07-30'),
    ('Greta Gerwig', '1983-08-04'),
    ('Bong Joon-ho', '1969-09-14'),
    ('Jordan Peele', '1979-02-21'),
]
people = {}
for name, birth in people_data:
    p, _ = Person.objects.get_or_create(name=name, defaults={'birth_date': birth})
    people[name] = p

# 4. Películas (10)
movies_data = [
    # title, year, genre_names, director, cast, duration, synopsis
    ('Dune', 2021, ['Ciencia ficción'], 'Denis Villeneuve',
     ['Denis Villeneuve'], 155, 'Paul Atreides viaja a Arrakis.'),
    ('Interstellar', 2014, ['Ciencia ficción', 'Drama'], 'Christopher Nolan',
     ['Christopher Nolan'], 169, 'Viaje interestelar para salvar a la humanidad.'),
    ('Barbie', 2023, ['Comedia'], 'Greta Gerwig',
     ['Greta Gerwig'], 114, 'Barbie descubre el mundo real.'),
    ('Parásitos', 2019, ['Drama'], 'Bong Joon-ho',
     ['Bong Joon-ho'], 132, 'Una familia pobre se infiltra en una rica.'),
    ('¡Huye!', 2017, ['Terror', 'Drama'], 'Jordan Peele',
     ['Jordan Peele'], 104, 'Un fin de semana que se tuerce.'),
    ('Arrival', 2016, ['Ciencia ficción', 'Drama'], 'Denis Villeneuve',
     ['Denis Villeneuve', 'Christopher Nolan'], 116, 'Una lingüista contacta alienígenas.'),
    ('El gran hotel Budapest', 2014, ['Comedia', 'Drama'], 'Greta Gerwig',
     ['Greta Gerwig'], 99, 'Aventuras de un conserje legendario.'),
    ('El conjuro', 2013, ['Terror'], 'Christopher Nolan',
     ['Jordan Peele'], 112, 'Expediente Warren.'),
    ('Her', 2013, ['Drama', 'Ciencia ficción'], 'Bong Joon-ho',
     ['Greta Gerwig'], 126, 'Un hombre se enamora de una IA.'),
    ('Zombieland', 2009, ['Comedia', 'Terror'], 'Jordan Peele',
     ['Jordan Peele', 'Greta Gerwig'], 88, 'Comedia de zombis.'),
]
movies = {}
for title, year, gnames, director, cast, duration, synopsis in movies_data:
    m, created = Movie.objects.get_or_create(
        title=title, year=year,
        defaults={
            'director': people[director],
            'duration_minutes': duration,
            'synopsis': synopsis,
        },
    )
    if created:
        m.director = people[director]
        m.duration_minutes = duration
        m.synopsis = synopsis
        m.save()
    m.genres.set([genres[g] for g in gnames])
    m.cast.set([people[c] for c in cast])
    movies[title] = m

# 5. Valoraciones en al menos 5 películas (aquí 6)
ratings_data = [
    ('Dune', 'Ana', 5, 'Espectacular.'),
    ('Dune', 'Luis', 4, 'Gran fotografía.'),
    ('Interstellar', 'Ana', 5, 'Obra maestra.'),
    ('Interstellar', 'Marta', 5, 'La mejor de Nolan.'),
    ('Interstellar', 'Luis', 4, 'Muy larga pero vale.'),
    ('Barbie', 'Marta', 4, 'Divertida y lúcida.'),
    ('Parásitos', 'Ana', 5, 'Imprescindible.'),
    ('Parásitos', 'Luis', 5, 'Guion perfecto.'),
    ('¡Huye!', 'Marta', 4, 'Tensión total.'),
    ('Arrival', 'Ana', 5, 'Ciencia ficción inteligente.'),
    ('Arrival', 'Luis', 3, 'Ritmo lento.'),
]
for title, reviewer, score, comment in ratings_data:
    Rating.objects.get_or_create(
        movie=movies[title], reviewer_name=reviewer, score=score,
        defaults={'comment': comment},
    )

# 6. Grupo «editores»: add + change película, SIN delete. Usuario editor.
group, _ = Group.objects.get_or_create(name='editores')
perms = Permission.objects.filter(
    codename__in=['add_movie', 'change_movie'],
    content_type__app_label='movies',
)
group.permissions.set(perms)

editor, created = User.objects.get_or_create(
    username='editor', defaults={'email': 'editor@example.com'},
)
editor.set_password('editor123')
editor.is_staff = True  # necesita entrar al admin
editor.is_superuser = False
editor.save()
editor.groups.add(group)

print('Seed movies OK')
print(f'Géneros: {Genre.objects.count()} | Personas: {Person.objects.count()}')
print(f'Películas: {Movie.objects.count()} | Valoraciones: {Rating.objects.count()}')
print(f'Películas con valoración: {Movie.objects.filter(ratings__isnull=False).distinct().count()}')
print(f'Grupo editores permisos: {sorted(p.codename for p in group.permissions.all())}')
print(f'Editor en grupo: {editor.groups.filter(name="editores").exists()} | is_staff={editor.is_staff}')
