"""Descarga pósters oficiales desde el CDN de TMDB (image.tmdb.org)
y los asigna a Movie.poster. Uso académico: © sus respectivos estudios.
"""
import os
import urllib.request
from pathlib import Path

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from PIL import Image  # noqa: E402

from movies.models import Movie  # noqa: E402

BASE = Path(__file__).resolve().parent
POSTERS = BASE / 'media' / 'posters'
POSTERS.mkdir(parents=True, exist_ok=True)

UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) LabDAE-academic'}

# (título BD, año, hash de póster en TMDB)
TARGETS = [
    ('Dune', 2021, '/d5NXSklXo0qyIYkgV94XAgMIckC.jpg'),
    ('Interstellar', 2014, '/gEU2QniE6E77NI6lCU6MxlNBvIx.jpg'),
    ('Barbie', 2023, '/iuFNMS8U5cb6xfzi51Dbkovj7vM.jpg'),
    ('Parásitos', 2019, '/7IiTTgloJzvGI1TAYymCfbfl3vT.jpg'),
    ('¡Huye!', 2017, '/tFXcEccSQMf3lfhfXKSU9iRBpae3.jpg'),
    ('Arrival', 2016, '/x2FJsf1ElAgr63Y3PNPtJrcmpoe.jpg'),
    ('El gran hotel Budapest', 2014, '/eWdyYQreja6JGCzqHWXpWHDrrPo.jpg'),
    ('El conjuro', 2013, '/wVYREutTvI2tmxr6ujrHT704wGF.jpg'),
    ('Her', 2013, '/lEIaL12hSkqqe83kgADkbUqEnvk.jpg'),
    ('Zombieland', 2009, '/qkp7T6v9sv5RyqOGX7h7qUu357p.jpg'),
]


def slug(s):
    return ''.join(c if c.isalnum() else '_' for c in s.lower())[:40].strip('_')


ok, fail = [], []
for title, year, phash in TARGETS:
    try:
        movie = Movie.objects.get(title=title, year=year)
    except Movie.DoesNotExist:
        fail.append((title, 'no está en BD'))
        continue
    try:
        src = f'https://image.tmdb.org/t/p/w500{phash}'
        fname = f'real_{year}_{slug(title)}.jpg'
        dest = POSTERS / fname
        req = urllib.request.Request(src, headers=UA)
        with urllib.request.urlopen(req, timeout=30) as r, open(dest, 'wb') as f:
            f.write(r.read())
        with Image.open(dest) as im:
            im.verify()
        with Image.open(dest) as im:
            size = im.size
        if size[0] < 100:
            raise ValueError(f'imagen sospechosa {size}')
        movie.poster.name = f'posters/{fname}'
        movie.save(update_fields=['poster'])
        ok.append(title)
        print(f'OK  {title} ({year}) {size}')
    except Exception as e:  # noqa: BLE001
        fail.append((title, str(e)))
        print(f'FAIL {title} ({year}): {e}')

print(f'\nPósters reales: {len(ok)}/{len(TARGETS)}')
for t, reason in fail:
    print(f'  pendiente: {t} ({reason})')
