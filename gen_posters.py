"""Genera pósters cinematográficos + avatares y los asigna a Movie/Person."""
import os
from pathlib import Path

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from PIL import Image, ImageDraw, ImageFont  # noqa: E402

from movies.models import Movie, Person  # noqa: E402

BASE = Path(__file__).resolve().parent
POSTERS = BASE / 'media' / 'posters'
PERSONS = BASE / 'media' / 'persons'
POSTERS.mkdir(parents=True, exist_ok=True)
PERSONS.mkdir(parents=True, exist_ok=True)

# Paleta por género principal (fondo degradado arriba -> abajo)
PALETTES = {
    'Ciencia ficción': ((15, 23, 42), (37, 99, 235)),
    'Drama': ((24, 10, 30), (190, 60, 90)),
    'Comedia': ((40, 20, 0), (245, 158, 11)),
    'Terror': ((5, 5, 10), (120, 20, 20)),
}
DEFAULT_PALETTE = ((20, 20, 35), (80, 80, 140))

W, H = 400, 600


def font(size):
    for name in ('arial.ttf', 'DejaVuSans-Bold.ttf', 'DejaVuSans.ttf'):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


def slug(s):
    return ''.join(c if c.isalnum() else '_' for c in s.lower())[:40].strip('_')


def gradient(size, top, bottom):
    img = Image.new('RGB', size, top)
    d = ImageDraw.Draw(img)
    for y in range(size[1]):
        t = y / (size[1] - 1)
        d.line([(0, y), (size[0], y)],
               fill=tuple(int(a + (b - a) * t) for a, b in zip(top, bottom)))
    return img


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ''
    for w in words:
        t = (cur + ' ' + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def make_poster(movie):
    genres = [g.name for g in movie.genres.all()]
    pal = PALETTES.get(genres[0] if genres else '', DEFAULT_PALETTE)
    img = gradient((W, H), *pal)
    d = ImageDraw.Draw(img)
    # viñeta + marco
    d.rectangle([0, 0, W - 1, H - 1], outline=(255, 255, 255, 90), width=3)
    d.rectangle([14, 14, W - 15, H - 15], outline=(255, 255, 255), width=1)
    # etiqueta género
    f_small = font(20)
    tag = ' · '.join(genres) if genres else 'CINE'
    d.text((30, 30), tag.upper()[:34], font=f_small, fill=(255, 220, 120))
    # título centrado
    f_title = font(44)
    lines = wrap(d, movie.title, f_title, W - 80)
    y = 200
    for line in lines[:3]:
        wline = d.textlength(line, font=f_title)
        d.text(((W - wline) / 2, y), line, font=f_title, fill='white')
        y += 56
    # año + director
    f_mid = font(26)
    year = str(movie.year)
    d.text(((W - d.textlength(year, font=f_mid)) / 2, y + 10), year, font=f_mid, fill=(255, 220, 120))
    if movie.director:
        f_dir = font(20)
        label = f'dir. {movie.director.name}'[:36]
        d.text(((W - d.textlength(label, font=f_dir)) / 2, H - 90), label, font=f_dir, fill=(230, 230, 240))
    # franja inferior
    d.rectangle([0, H - 46, W, H], fill=(0, 0, 0))
    f_bot = font(18)
    avg = movie.avg_rating
    stars = '★' * round(avg) + '☆' * (5 - round(avg)) if avg else '☆☆☆☆☆'
    txt = f'{stars}  {avg:.1f}' if avg else 'SIN VOTOS'
    d.text(((W - d.textlength(txt, font=f_bot)) / 2, H - 36), txt, font=f_bot, fill=(255, 210, 63))
    fname = f"{movie.year}_{slug(movie.title)}.jpg"
    path = POSTERS / fname
    img.save(path, 'JPEG', quality=88)
    return f'posters/{fname}'


def make_avatar(person):
    initials = ''.join(p[0] for p in person.name.split()[:2]).upper()
    img = gradient((300, 300), (30, 30, 60), (90, 60, 160))
    d = ImageDraw.Draw(img)
    d.ellipse([70, 60, 230, 220], fill=(255, 255, 255))
    f = font(80)
    tw = d.textlength(initials, font=f)
    d.text(((300 - tw) / 2, 105), initials, font=f, fill=(40, 40, 90))
    f2 = font(20)
    name = person.name[:22]
    d.text(((300 - d.textlength(name, font=f2)) / 2, 245), name, font=f2, fill='white')
    fname = f"{slug(person.name)}.jpg"
    path = PERSONS / fname
    img.save(path, 'JPEG', quality=85)
    return f'persons/{fname}'


n_posters = 0
for m in Movie.objects.prefetch_related('genres').select_related('director'):
    rel = make_poster(m)
    if m.poster.name != rel:
        m.poster.name = rel
        m.save(update_fields=['poster'])
        n_posters += 1

n_avatars = 0
for p in Person.objects.all():
    rel = make_avatar(p)
    if p.photo.name != rel:
        p.photo.name = rel
        p.save(update_fields=['photo'])
        n_avatars += 1

print(f'Posters generados: {n_posters} | Avatares: {n_avatars}')
print(f'Películas con póster: {Movie.objects.exclude(poster="").count()}/{Movie.objects.count()}')
