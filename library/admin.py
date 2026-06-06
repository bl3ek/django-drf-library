from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Reader, Author, Book, Borrowing

# Налаштування для читачів (кастомного User)
@admin.register(Reader)
class ReaderAdmin(UserAdmin):
    list_display = ('username', 'email', 'phone', 'registration_date', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        ('Додаткова інформація', {'fields': ('phone', 'address')}),
    )

# Налаштування для авторів
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'birth_date', 'book_count')
    search_fields = ('name',)

# Налаштування для книг
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'isbn', 'available_copies')
    list_filter = ('author', 'published_date')
    search_fields = ('title', 'isbn')

# Налаштування для позик
@admin.register(Borrowing)
class BorrowingAdmin(admin.ModelAdmin):
    list_display = ('book', 'reader', 'borrowed_date', 'is_returned')
    list_filter = ('is_returned', 'borrowed_date')
    search_fields = ('book__title', 'reader__username')