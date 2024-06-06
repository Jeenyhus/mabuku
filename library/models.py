from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class Profile(models.Model):
    """
    A model to store user profile information
    
    Attributes:
    user (OneToOneField): A reference to the User model
    address (CharField): The address of the user
    phone (CharField): The phone number of the user
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(_("Address"), max_length=255)
    phone = models.CharField(_("Phone"), max_length=20)

    def __str__(self):
        return f'{self.user.username} Profile'

class Member(models.Model):
    """
    A model to store member information
    
    Attributes:
    profile (OneToOneField): A reference to the Profile model
    date_of_membership (DateField): The date of membership of the member
    """
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    date_of_membership = models.DateField(_("Date of Membership"))

    def get_total_checked_out_books(self):
        return BookLending.objects.filter(member=self, return_date__isnull=True).count()

class Librarian(models.Model):
    """
    A model to store librarian information
    
    Attributes:
    profile (OneToOneField): A reference to the Profile model
    """
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)

    def add_book_item(self, book_item):
        book_item.save()

    def block_member(self, member):
        member.profile.user.is_active = False
        member.profile.user.save()

    def unblock_member(self, member):
        member.profile.user.is_active = True
        member.profile.user.save()

class Author(models.Model):
    """
    A model to store author information
    
    Attributes:
    name (CharField): The name of the author
    description (TextField): A description of the author
    """
    name = models.CharField(_("Name"), max_length=100)
    description = models.TextField(_("Description"))

    def get_name(self):
        return self.name

class Genre(models.Model):
    """
    A model to store genre information
    
    Attributes: 
    name (CharField): The name of the genre
    """
    name = models.CharField(_("Name"), max_length=50)

    def __str__(self):
        return self.name

class Book(models.Model):
    """
    A model to store book information
    
    Attributes:
    ISBN (CharField): The ISBN of the book
    title (CharField): The title of the book
    subject (CharField): The subject of the book
    publisher (CharField): The publisher of the book
    language (CharField): The language of the book
    number_of_pages (IntegerField): The number of pages in the book 
    author (ForeignKey): A reference to the Author model
    genre (ForeignKey): A reference to the Genre model
    """
    ISBN = models.CharField(_("ISBN"), max_length=13, unique=True)
    title = models.CharField(_("Title"), max_length=100)
    subject = models.CharField(_("Subject"), max_length=100)
    publisher = models.CharField(_("Publisher"), max_length=100)
    language = models.CharField(_("Language"), max_length=30)
    number_of_pages = models.IntegerField(_("Number of Pages"))
    author = models.ForeignKey(Author, verbose_name=_("Author"), on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, verbose_name=_("Genre"), on_delete=models.CASCADE)

    def get_title(self):
        return self.title

class Rack(models.Model):
    """
    A model to store rack information
    
    Attributes:
    number (IntegerField): The number of the rack
    location_identifier (CharField): The location identifier of the rack
    """
    number = models.IntegerField(_("Number"))
    location_identifier = models.CharField(_("Location Identifier"), max_length=100)

class BookItem(models.Model):
    """
    A model to store book item information
    
    Attributes:
    barcode (CharField): The barcode of the book item
    is_reference_only (BooleanField): A boolean field to indicate if the book item is reference only
    borrowed (BooleanField): A boolean field to indicate if the book item is borrowed
    due_date (DateField): The due date of the book item
    price (DecimalField): The price of the book item
    format (CharField): The format of the book item
    status (CharField): The status of the book item
    date_of_purchase (DateField): The date of purchase of the book item
    publication_date (DateField): The publication date of the book item
    book (ForeignKey): A reference to the Book model
    rack (ForeignKey): A reference to the Rack model
    """
    barcode = models.CharField(_("Barcode"), max_length=100, unique=True)
    is_reference_only = models.BooleanField(_("Is Reference Only"), default=False)
    borrowed = models.BooleanField(_("Borrowed"), default=False)
    due_date = models.DateField(_("Due Date"), null=True, blank=True)
    price = models.DecimalField(_("Price"), max_digits=6, decimal_places=2)
    format = models.CharField(_("Format"), max_length=20, choices=[
        ('Hardcover', 'Hardcover'),
        ('Paperback', 'Paperback'),
        ('Audiobook', 'Audiobook'),
        ('Ebook', 'Ebook'),
        ('Newspaper', 'Newspaper'),
        ('Magazine', 'Magazine'),
        ('Journal', 'Journal'),
    ])
    status = models.CharField(_("Status"), max_length=20, choices=[
        ('Available', 'Available'),
        ('Reserved', 'Reserved'),
        ('Lost', 'Lost'),
    ])
    date_of_purchase = models.DateField(_("Date of Purchase"))
    publication_date = models.DateField(_("Publication Date"))
    book = models.ForeignKey(Book, verbose_name=_("Book"), on_delete=models.CASCADE)
    rack = models.ForeignKey(Rack, verbose_name=_("Rack"), on_delete=models.CASCADE)

    def checkout(self):
        self.borrowed = True
        self.save()

class Library(models.Model):
    """
    A model to store library information
    
    Attributes:
    name (CharField): The name of the library
    address (CharField): The address of the library
    """
    name = models.CharField(_("Name"), max_length=100)
    address = models.CharField(_("Address"), max_length=255)

    def get_address(self):
        return self.address

class LibraryCard(models.Model):
    """
    A model to store library card information
    
    Attributes:
    card_number (CharField): The card number of the library card
    issued_at (DateField): The date the library card was issued
    active (BooleanField): A boolean field to indicate if the library card is active

    """
    card_number = models.CharField(_("Card Number"), max_length=100, unique=True)
    issued_at = models.DateField(_("Issued At"))
    active = models.BooleanField(_("Active"), default=True)

class BookReservation(models.Model):
    """
    A model to store book reservation information
    
    Attributes:
    reservation_date (DateField): The reservation date of the book
    status (CharField): The status of the reservation
    book_item (ForeignKey): A reference to the BookItem model
    member (ForeignKey): A reference to the Member model
    """
    reservation_date = models.DateField(_("Reservation Date"), auto_now_add=True)
    status = models.CharField(_("Status"), max_length=20, choices=[
        ('Waiting', 'Waiting'),
        ('Pending', 'Pending'),
        ('Canceled', 'Canceled'),
        ('Completed', 'Completed'),
        ('None', 'None'),
    ])
    book_item = models.ForeignKey(BookItem, verbose_name=_("Book Item"), on_delete=models.CASCADE)
    member = models.ForeignKey(Member, verbose_name=_("Member"), on_delete=models.CASCADE)

    def set_status(self, status):
        self.status = status
        self.save()

    def fetch_reservation_details(self):
        return {
            "reservation_date": self.reservation_date,
            "status": self.status,
            "book_item": self.book_item,
            "member": self.member
        }

class BookLending(models.Model):
    """
    A model to store book lending information
    
    Attributes:
    creation_date (DateField): The creation date of the book lending
    due_date (DateField): The due date of the book lending
    return_date (DateField): The return date of the book lending
    book_item (ForeignKey): A reference to the BookItem model
    member (ForeignKey): A reference to the Member model
    """
    creation_date = models.DateField(_("Creation Date"), auto_now_add=True)
    due_date = models.DateField(_("Due Date"))
    return_date = models.DateField(_("Return Date"), null=True, blank=True)
    book_item = models.ForeignKey(BookItem, verbose_name=_("Book Item"), on_delete=models.CASCADE)
    member = models.ForeignKey(Member, verbose_name=_("Member"), on_delete=models.CASCADE)

    def get_return_date(self):
        return self.return_date

class Catalog(models.Model):
    """
    A model to store catalog information
    
    Attributes:
    creation_date (DateField): The creation date of the catalog
    total_books (IntegerField): The total number of books in the catalog
    book_titles (JSONField): A JSON field to store book titles
    book_authors (JSONField): A JSON field to store book authors
    book_subjects (JSONField): A JSON field to store book subjects
    book_publication_dates (JSONField): A JSON field to store book publication dates
    """
    creation_date = models.DateField(_("Creation Date"))
    total_books = models.IntegerField(_("Total Books"))
    book_titles = models.JSONField(_("Book Titles"))
    book_authors = models.JSONField(_("Book Authors"))
    book_subjects = models.JSONField(_("Book Subjects"))
    book_publication_dates = models.JSONField(_("Book Publication Dates"))

    def update_catalog(self):
        # logic to update the catalog
        pass

class Notification(models.Model):
    """
    A model to store notification information
    
    Attributes:
    notification_id (AutoField): The notification ID
    created_on (DateTimeField): The date and time the notification was created
    content (TextField): The content of the notification
    member (ForeignKey): A reference to the Member model
    """
    notification_id = models.AutoField(_("Notification ID"), primary_key=True)
    created_on = models.DateTimeField(_("Created On"), auto_now_add=True)
    content = models.TextField(_("Content"))
    member = models.ForeignKey(Member, verbose_name=_("Member"), on_delete=models.CASCADE)

    def send_notification(self):
        # logic to send notification

        pass

class PostalNotification(Notification):
    """
    A model to store postal notification information
    
    Attributes:
    address (CharField): The address of the recipient
    """
    address = models.CharField(_("Address"), max_length=255)

class EmailNotification(Notification):
    """
    A model to store email notification information
    
    Attributes:
    email (EmailField): The email of the recipient
    """
    email = models.EmailField(_("Email"))

class BarcodeReader(models.Model):
    """
    A model to store barcode reader information
    
    Attributes:
    barcode (CharField): The barcode of the barcode reader
    registered_at (DateField): The date the barcode reader was registered
    active (BooleanField): A boolean field to indicate if the barcode reader is active
    """
    barcode = models.CharField(_("Barcode"), max_length=100, unique=True)
    registered_at = models.DateField(_("Registered At"))
    active = models.BooleanField(_("Active"), default=True)

    def is_active(self):
        return self.active

class Account(models.Model):
    """
    A model to store account information
    
    Attributes:
    password (CharField): The password of the account
    status (CharField): The status of the account
    profile (OneToOneField): A reference to the Profile model
    """
    id = models.AutoField(_("ID"), primary_key=True)
    password = models.CharField(_("Password"), max_length=128)
    status = models.CharField(_("Status"), max_length=20, choices=[
        ('Active', 'Active'),
        ('Closed', 'Closed'),
        ('Canceled', 'Canceled'),
        ('Blacklisted', 'Blacklisted'),
        ('None', 'None'),
    ])
    profile = models.OneToOneField(Profile, verbose_name=_("Profile"), on_delete=models.CASCADE)

    def reset_password(self, new_password):
        self.password = new_password
        self.save()

class Transaction(models.Model):
    """
    A model to store transaction information
    
    Attributes:
    creation_date (DateField): The creation date of the transaction
    amount (DecimalField): The amount of the transaction
    """
    creation_date = models.DateField(_("Creation Date"))
    amount = models.DecimalField(_("Amount"), max_digits=10, decimal_places=2)

    def get_amount(self):
        return self.amount

class FineTransaction(Transaction):
    """
    A model to store fine transaction information
    
    Attributes:
    reason (CharField): The reason for the fine transaction
    """
    pass

class CreditCardTransaction(Transaction):
    """
    A model to store credit card transaction information
    
    Attributes:
    name_on_card (CharField): The name on the card
    """
    name_on_card = models.CharField(_("Name on Card"), max_length=100)

class CheckTransaction(Transaction):
    """
    A model to store check transaction information
    
    Attributes:
    bank_name (CharField): The bank name
    check_number (CharField): The check number
    """
    bank_name = models.CharField(_("Bank Name"), max_length=100)
    check_number = models.CharField(_("Check Number"), max_length=100)

class CashTransaction(Transaction):
    """
    A model to store cash transaction information
    
    Attributes:
    cash_tendered (DecimalField): The cash tendered
    """
    cash_tendered = models.DecimalField(_("Cash Tendered"), max_digits=10, decimal_places=2)
