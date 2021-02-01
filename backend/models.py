from django.db import models
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .utils import get_random_id
import uuid
import barcode
from barcode.writer import ImageWriter
from io import BytesIO
from django.core.files import File
# Create your models here.
class Member(models.Model):
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    email = models.EmailField(max_length=50,blank=True )
    avatar = models.ImageField(default="avatar.jpg", upload_to="avatar/", blank=True)
    updated_at = models.DateTimeField(auto_now = True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # return f"{self.user.username}--{self.created_at.strftime('%d-%m-%y%y')}"
        return self.user.username

class BookEntry(models.Model):
    class Meta:
        verbose_name_plural = 'Book Entry'
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    summary = models.TextField(max_length=1000, help_text="Enter a brief description of the book")
    isbn = models.IntegerField(primary_key=True,
                            help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    genre = models.TextField(max_length=20, help_text="For example: science, History, Technical, Enclyclopedia, etc.", null=True)
    language = models.TextField(max_length=20)
    total_copies = models.IntegerField()
    available_copies = models.IntegerField()
    pic = models.ImageField(blank=True, null=True, upload_to='book_image')
    published_year = models.DateField(null=True)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

def get_expiry():
    return datetime.today() + timedelta(days=15)

class BookIssue(models.Model):
    class Meta:
        verbose_name_plural = 'Book Issue'
    issue_book_name = models.CharField(max_length=200)
    isbn = models.ForeignKey(BookEntry, on_delete=models.CASCADE)
    member_name = models.CharField(max_length=200)
    member_id = models.ForeignKey(Member, on_delete=models.CASCADE)
    issue_date = models.DateTimeField(auto_now_add=True)
    expirydate = models.DateField(default=get_expiry)
    
    def __str__(self):
        return str(self.issue_book_name) + "[" + str(self.isbn) + ']'

class BookReturn(models.Model):
    title = models.CharField(max_length=200)
    isbn = models.ForeignKey(BookIssue, on_delete=models.CASCADE)
    member_name = models.CharField(max_length=200)
    member_id = models.ForeignKey(Member, on_delete=models.CASCADE)
    return_date = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.title) + "[" + str(self.isbn) + ']'

class BookRenew(models.Model):
    title = models.CharField(max_length=200)
    isbn = models.ForeignKey(BookIssue, on_delete=models.CASCADE)
    member_name = models.CharField(max_length=200)
    member_id = models.ForeignKey(Member, on_delete=models.CASCADE)
    renew_date = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now=True)
    expirydate = models.DateField(default=get_expiry)

    def __str__(self):
        return str(self.title) + "[" + str(self.isbn) + ']'

class Barcode(models.Model):
    name = models.CharField(max_length=100)
    barcode = models.ImageField(upload_to = 'barcode_images/', blank = True)
    country_id = models.CharField(max_length=2)
    manufacturer_id = models.CharField(max_length=6)
    product_id = models.CharField(max_length=5)

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        ISBN = barcode.get_barcode_class('isbn13')
        isbn = ISBN(f'{self.country_id}{self.manufacturer_id}{self.product_id}', writer=ImageWriter())
        buffer = BytesIO()
        isbn.write(buffer)
        self.barcode.save(f'{self.name}.png', File(buffer), save=False)
        return super().save(*args, **kwargs)
    

