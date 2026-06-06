from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date

# 1. Модель Читача (Кастомний користувач)
class Reader(AbstractUser):
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    registration_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.username


# 2. Модель Автора
class Author(models.Model):
    name = models.CharField(max_length=200)
    bio = models.TextField()
    birth_date = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='authors/', blank=True, null=True)

    def __str__(self):
        return self.name

    @property
    def book_count(self):
        return self.books.count()


# 3. Модель Книги
class Book(models.Model):
    title = models.CharField(max_length=300)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    description = models.TextField()
    isbn = models.CharField(max_length=13, unique=True)
    published_date = models.DateField()
    pages = models.PositiveIntegerField()
    cover = models.ImageField(upload_to='books/', blank=True, null=True)
    available_copies = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.title

    @property
    def is_available(self):
        return self.available_copies > 0


# 4. Модель Позики Книги
class Borrowing(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='borrowings')
    reader = models.ForeignKey(Reader, on_delete=models.CASCADE, related_name='borrowings')
    borrowed_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(blank=True, null=True)
    is_returned = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.reader.username} позичив книгу '{self.book.title}'"

    @property
    def days_borrowed(self):
        if self.is_returned and self.return_date:
            delta = self.return_date - self.borrowed_date
        else:
            delta = date.today() - self.borrowed_date
        return delta.days