import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()

from library.models import Author, Book, Category, Publisher, Publication

print('=== Step 9: Django Console Queries ===')
print()

# Query 1: libro.autor (forward)
print('1. libro.autor (forward):')
book1 = Book.objects.get(title="Harry Potter and the Philosopher's Stone")
print(f'   Book: {book1.title} -> Author: {book1.author.name}')
print()

# Query 2: autor.libros.all() (backward)
print('2. autor.libros.all() (backward):')
author1 = Author.objects.get(name='J.K. Rowling')
print(f'   Author: {author1.name} -> Books: {author1.books.count()}')
for b in author1.books.all():
    print(f'     - {b.title}')
print()

# Query 3: filtrado con doble guion bajo
print('3. filtrado con doble guion bajo:')
books_rowling = Book.objects.filter(author__name='J.K. Rowling')
print(f'   Books by J.K. Rowling: {books_rowling.count()}')
for b in books_rowling:
    print(f'     - {b.title}')
print()

# Query 4: filtrar por categoria
print('4. filtrar por categoria:')
fantasy_books = Book.objects.filter(categories__name='Fantasy')
print(f'   Fantasy books: {fantasy_books.count()}')
for b in fantasy_books:
    print(f'     - {b.title}')
print()

# Query 5: filtrar por editorial
print('5. filtrar por editorial:')
penguin_books = Book.objects.filter(publisher__name='Penguin')
print(f'   Penguin books: {penguin_books.count()}')
for b in penguin_books:
    print(f'     - {b.title}')
print()

# Query 6: Book with two categories
print('6. Book in two categories (Clash of Kings):')
book4 = Book.objects.get(title='A Clash of Kings')
print(f'   Book: {book4.title}')
print(f'   Categories: {[c.name for c in book4.categories.all()]}')
print()