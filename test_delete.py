import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

from library.models import Author, Book
import sqlite3

# Test 1: Delete author with books (using CASCADE default)
print('=== Test 1: Delete author with books (CASCADE) ===')
author1 = Author.objects.get(name='J.K. Rowling')
print(f'Author: {author1.name}')
print(f'Books before delete: {author1.books.count()}')
author1.delete()
print(f'Books after delete: {Book.objects.count()}')
print('Tables after delete:')
conn = sqlite3.connect('db.sqlite3')
c = conn.cursor()
c.execute("SELECT name FROM sqlite_master WHERE type='table'")
for row in c.fetchall():
    print(f'  {row[0]}')
conn.close()
print()