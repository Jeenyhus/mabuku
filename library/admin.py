from django.contrib import admin
from .models import Book, Genre, Librarian, Member, BookItem, LibraryCard, BookReservation, BookLending, Catalog, Author, Rack, Library, Notification, PostalNotification, EmailNotification, BarcodeReader, Account, Transaction, FineTransaction, CreditCardTransaction, CheckTransaction, CashTransaction
# Register your models here.

admin.site.register(Book)
admin.site.register(Genre)
admin.site.register(Librarian)
admin.site.register(Member)
admin.site.register(BookItem)
admin.site.register(LibraryCard)
admin.site.register(BookReservation)
admin.site.register(BookLending)
admin.site.register(Author)
admin.site.register(Rack)
admin.site.register(Library)
admin.site.register(Notification)
admin.site.register(PostalNotification)
admin.site.register(EmailNotification)
admin.site.register(BarcodeReader)
admin.site.register(Account)
admin.site.register(Transaction)
admin.site.register(FineTransaction)
admin.site.register(CreditCardTransaction)
admin.site.register(CheckTransaction)
admin.site.register(CashTransaction)