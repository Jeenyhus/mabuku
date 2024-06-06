from django.contrib import admin
from .models import Book, Genre, Librarian, Member, BookItem, LibraryCard, BookReservation, BookLending
# Register your models here.

admin.site.register(Book)
admin.site.register(Genre)
admin.site.register(Librarian)
admin.site.register(Member)
admin.site.register(BookItem)
admin.site.register(LibraryCard)
admin.site.register(BookReservation)
admin.site.register(BookLending)