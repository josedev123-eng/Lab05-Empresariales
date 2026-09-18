import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
os.environ['DJANGO_SUPERUSER_PASSWORD'] = 'admin123'

import django
django.setup()

from library.models import Author, Book, Publisher, Category, Publication

# Create authors
author1 = Author.objects.create(name='J.K. Rowling', email='jkrowling1@example.com', birth_date='1965-07-31')
author2 = Author.objects.create(name='George R.R. Martin', email='grrm1@example.com', birth_date='1948-09-20')

# Create publishers
publisher1 = Publisher.objects.create(name='Bloomsbury', website='https://www.bloomsbury.com')
publisher2 = Publisher.objects.create(name='Penguin Random House', website='https://www.penguinrandomhouse.com')

# Create categories
category1 = Category.objects.create(name='Fantasy', description='Magic and imaginary worlds')
category2 = Category.objects.create(name='Science Fiction', description='Future technology and space')
category3 = Category.objects.create(name='Mystery', description='Crimes and investigations')

# Create books
book1 = Book.objects.create(
    title='Harry Potter and the Philosopher\'s Stone',
    author=author1,
    publisher=publisher1,
    publication_date='1997-06-26',
    isbn='9780747532699',
    price=15.99
)
book2 = Book.objects.create(
    title='Harry Potter and the Chamber of Secrets',
    author=author1,
    publisher=publisher1,
    publication_date='1998-07-02',
    isbn='9780747535562',
    price=14.99
)
book3 = Book.objects.create(
    title='A Game of Thrones',
    author=author2,
    publisher=publisher2,
    publication_date='1996-08-06',
    isbn='9780553103540',
    price=19.99
)
book4 = Book.objects.create(
    title='A Clash of Kings',
    author=author2,
    publisher=publisher2,
    publication_date='1998-11-16',
    isbn='9780553108035',
    price=21.99
)

# Create Publication records (through model) - book4 will be in two categories
Publication.objects.create(book=book1, publisher=publisher1, category=category1, edition=1, publication_date='1997-06-26')
Publication.objects.create(book=book2, publisher=publisher1, category=category1, edition=1, publication_date='1998-07-02')
Publication.objects.create(book=book3, publisher=publisher2, category=category2, edition=1, publication_date='1996-08-06')
Publication.objects.create(book=book4, publisher=publisher2, category=category2, edition=1, publication_date='1998-11-16')
Publication.objects.create(book=book4, publisher=publisher2, category=category3, edition=1, publication_date='1998-11-16')

# Also add many-to-many relationships through the admin/ORM way
# The Publication records above already establish the M2M connections
# But we need to also ensure the M2M field works - let's add through the field
book1.categories.add(category1, through_defaults={'edition': 1})
book2.categories.add(category1, through_defaults={'edition': 1})
book3.categories.add(category2, through_defaults={'edition': 1})
book4.categories.add(category2, through_defaults={'edition': 1})
book4.categories.add(category3, through_defaults={'edition': 1})

print("Test data seeded successfully!")
print(f"Authors: {Author.objects.count()}")
print(f"Books: {Book.objects.count()}")
print(f"Categories: {Category.objects.count()}")
print(f"Publishers: {Publisher.objects.count()}")
print(f"Publications: {Publication.objects.count()}")

# Verify book4 is in two categories
book4_cat = book4.categories.all()
print(f"Book4 categories: {[c.name for c in book4_cat]}")
print(f"Book4 category count: {book4_cat.count()}")