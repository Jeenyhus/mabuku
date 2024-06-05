from django.contrib import admin
from .models import Book, Genre, Librarian, Member
# Register your models here.

admin.site.register(Book)
admin.site.register(Genre)
admin.site.register(Librarian)
admin.site.register(Member)