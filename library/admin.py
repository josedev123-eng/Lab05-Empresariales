from django.contrib import admin
from .models import Author, Book, Publisher, Category, Publication


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name', 'email']
    search_fields = ['name', 'email']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ['name', 'website']
    search_fields = ['name', 'website']


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'publisher']


@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    list_display = ['book', 'category', 'publisher', 'edition']

# Register your models here.
