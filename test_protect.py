import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()

from library.models import Author, Book
import sqlite3

# Test with PROTECT - try to delete author with books
print('=== Test: Delete author with books (PROTECT) ===')
author2 = Author.objects.get(email='grrm@example.com')
print(f'Author: {author2.name}')
print(f'Books by author: {author2.books.count()}')
try:
    author2.delete()
    print('Author deleted successfully (UNEXPECTED with PROTECT)')
except Exception as e:
    print(f'Error deleting author: {e}')
    print('PROTECT is working - author was not deleted')

# Check books still exist
print(f'Books still exist: {Book.objects.count()}')

# Now test CASCADE behavior for comparison
print()
print('=== Test: Delete author with books (CASCADE) ===')
# Create a new author with books for CASCADE test
author1 = Author.objects.create(name='Test Author', email='test@example.com')
book_for_cascade = Book.objects.create(
    title='Test Book',
    author=author1,
    publication_date='2020-01-01',
    isbn='1111111111111',
    price=10.99
)
print(f'Books before CASCADE delete: {author1.books.count()}')
author1.delete()
print(f'Books after CASCADE delete: {Book.objects.count()}')
print('CASCADE worked - book was deleted along with author')