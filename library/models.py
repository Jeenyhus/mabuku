from django.db import models
from django.utils.translation import gettext_lazy as _

# Member Model
class Member(models.Model):
    first_name = models.CharField(_("First Name"), max_length=50)
    last_name = models.CharField(_("Last Name"), max_length=50)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

# Librarian Model
class Librarian(models.Model):
    first_name = models.CharField(_("First Name"), max_length=50)
    last_name = models.CharField(_("Last Name"), max_length=50)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

# Genre Model
class Genre(models.Model):
    name = models.CharField(_("Name"), max_length=50)

    def __str__(self):
        return self.name

# Book Model
class Book(models.Model):
    title = models.CharField(_("Title"), max_length=100)
    author = models.CharField(_("Author"), max_length=100)
    genre = models.ForeignKey(Genre, verbose_name=_("Genre"), on_delete=models.CASCADE)

    def __str__(self):
        return self.title

# BookItem Model
class BookItem(models.Model):
    book = models.ForeignKey(Book, verbose_name=_("Book"), on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)

# LibraryCard Model
class LibraryCard(models.Model):
    card_number = models.CharField(_("Card Number"), max_length=100)

    def __str__(self):
        return self.card_number

# BookReservation Model
class BookReservation(models.Model):
    book_item = models.ForeignKey(BookItem, verbose_name=_("Book Item"), on_delete=models.CASCADE)
    member = models.ForeignKey(Member, verbose_name=_("Member"), on_delete=models.CASCADE)
    reservation_date = models.DateField(_("Reservation Date"), auto_now_add=True)

# BookLending Model
class BookLending(models.Model):
    book_item = models.ForeignKey(BookItem, verbose_name=_("Book Item"), on_delete=models.CASCADE)
    member = models.ForeignKey(Member, verbose_name=_("Member"), on_delete=models.CASCADE)
    lending_date = models.DateField(_("Lending Date"), auto_now_add=True)

# Catalog Model
class Catalog(models.Model):
    SEARCH_CHOICES = [
        ("Title", _("Title")),
        ("Author", _("Author")),
        ("Subject", _("Subject")),
        ("Publish Date", _("Publish Date"))
    ]
    search_by = models.CharField(_("Search By"), max_length=20, choices=SEARCH_CHOICES)
    keyword = models.CharField(_("Keyword"), max_length=100)

# Library Model
class Library(models.Model):
    name = models.CharField(_("Name"), max_length=100)
    address = models.CharField(_("Address"), max_length=255)

    def __str__(self):
        return self.name

# Rack Model
class Rack(models.Model):
    rack_number = models.IntegerField(_("Rack Number"))
    location = models.CharField(_("Location"), max_length=255)

# Notification Model
class Notification(models.Model):
    member = models.ForeignKey(Member, verbose_name=_("Member"), on_delete=models.CASCADE)
    message = models.TextField(_("Message"))
    sent_date = models.DateTimeField(_("Sent Date"), auto_now_add=True)
