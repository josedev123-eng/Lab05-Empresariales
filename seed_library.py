import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

from django.contrib.auth.models import User
from library.models import Author, AuthorProfile, Book, Publisher, Category, Publication

# Admin (idempotente): crea o actualiza admin / admin123
admin, _ = User.objects.get_or_create(
    username='admin',
    defaults={'email': 'admin@example.com', 'is_staff': True, 'is_superuser': True},
)
admin.set_password('admin123')
admin.is_staff = True
admin.is_superuser = True
admin.save()

# Autores (2)
author1, _ = Author.objects.get_or_create(
    email='jkrowling1@example.com',
    defaults={'name': 'J.K. Rowling', 'birth_date': '1965-07-31'},
)
author2, _ = Author.objects.get_or_create(
    email='grrm1@example.com',
    defaults={'name': 'George R.R. Martin', 'birth_date': '1948-09-20'},
)

# Perfiles de autor (OneToOne)
AuthorProfile.objects.get_or_create(
    author=author1,
    defaults={'biography': 'British author, best known for the Harry Potter fantasy series.'},
)
AuthorProfile.objects.get_or_create(
    author=author2,
    defaults={'biography': 'American novelist, author of A Song of Ice and Fire.'},
)

# Editoriales (2)
publisher1, _ = Publisher.objects.get_or_create(
    name='Bloomsbury', defaults={'website': 'https://www.bloomsbury.com'},
)
publisher2, _ = Publisher.objects.get_or_create(
    name='Penguin Random House', defaults={'website': 'https://www.penguinrandomhouse.com'},
)

# Categorias (3)
category1, _ = Category.objects.get_or_create(
    name='Fantasy', defaults={'description': 'Magic and imaginary worlds'},
)
category2, _ = Category.objects.get_or_create(
    name='Science Fiction', defaults={'description': 'Future technology and space'},
)
category3, _ = Category.objects.get_or_create(
    name='Mystery', defaults={'description': 'Crimes and investigations'},
)

# Libros (4)
book1, _ = Book.objects.get_or_create(
    isbn='9780747532699',
    defaults={'title': "Harry Potter and the Philosopher's Stone", 'author': author1,
              'publisher': publisher1, 'publication_date': '1997-06-26', 'price': 15.99},
)
book2, _ = Book.objects.get_or_create(
    isbn='9780747535562',
    defaults={'title': 'Harry Potter and the Chamber of Secrets', 'author': author1,
              'publisher': publisher1, 'publication_date': '1998-07-02', 'price': 14.99},
)
book3, _ = Book.objects.get_or_create(
    isbn='9780553103540',
    defaults={'title': 'A Game of Thrones', 'author': author2,
              'publisher': publisher2, 'publication_date': '1996-08-06', 'price': 19.99},
)
book4, _ = Book.objects.get_or_create(
    isbn='9780553108035',
    defaults={'title': 'A Clash of Kings', 'author': author2,
              'publisher': publisher2, 'publication_date': '1998-11-16', 'price': 21.99},
)

# Publication (through): cada fila conecta book+category+publisher con edicion y fecha.
# Estas filas SON la relacion M2M (no se usa .add() aparte para evitar duplicados).
Publication.objects.get_or_create(book=book1, category=category1, publisher=publisher1,
                                  defaults={'edition': 1, 'publication_date': '1997-06-26'})
Publication.objects.get_or_create(book=book2, category=category1, publisher=publisher1,
                                  defaults={'edition': 1, 'publication_date': '1998-07-02'})
Publication.objects.get_or_create(book=book3, category=category2, publisher=publisher2,
                                  defaults={'edition': 1, 'publication_date': '1996-08-06'})
Publication.objects.get_or_create(book=book4, category=category2, publisher=publisher2,
                                  defaults={'edition': 1, 'publication_date': '1998-11-16'})
Publication.objects.get_or_create(book=book4, category=category3, publisher=publisher2,
                                  defaults={'edition': 1, 'publication_date': '1998-11-16'})

print("Test data seeded successfully!")
print(f"Authors: {Author.objects.count()} | Profiles: {AuthorProfile.objects.count()}")
print(f"Books: {Book.objects.count()}")
print(f"Categories: {Category.objects.count()}")
print(f"Publishers: {Publisher.objects.count()}")
print(f"Publications: {Publication.objects.count()}")

book4_cat = book4.categories.all()
print(f"Book4 categories: {[c.name for c in book4_cat]}")
print(f"Book4 category count: {book4_cat.count()}")
