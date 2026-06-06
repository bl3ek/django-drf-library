from rest_framework import serializers
from .models import Author, Book, Borrowing

# 1. Серіалізатор для Автора
class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name', 'bio', 'birth_date', 'photo']


# 2. Серіалізатор для Книги з валідацією полів
class BookSerializer(serializers.ModelSerializer):
    # Оскільки is_available — це @property в моделі, вказуємо його як read_only
    is_available = serializers.BooleanField(read_only=True)

    class Meta:
        model = Book
        fields = [
            'id', 'title', 'author', 'description', 'isbn', 
            'published_date', 'pages', 'cover', 'available_copies', 'is_available'
        ]

    # Валідація: кількість сторінок має бути більше 0
    def validate_pages(self, value):
        if value <= 0:
            raise serializers.ValidationError("Кількість сторінок має бути більшою за 0.")
        return value

    # Валідація: ISBN має містити рівно 13 символів
    def validate_isbn(self, value):
        if len(value) != 13:
            raise serializers.ValidationError("ISBN має містити рівно 13 символів.")
        return value


# 3. Серіалізатор для Позики (з вираховуваними та вкладеними полями)
class BorrowingSerializer(serializers.ModelSerializer):
    book_title = serializers.CharField(source='book.title', read_only=True)
    reader_name = serializers.CharField(source='reader.username', read_only=True)
    days_borrowed = serializers.SerializerMethodField()

    class Meta:
        model = Borrowing
        fields = ['id', 'book_title', 'reader_name', 'borrowed_date', 'return_date', 'is_returned', 'days_borrowed']

    def get_days_borrowed(self, obj):
        return obj.days_borrowed


# 4. БОНУС: Детальний серіалізатор для книги
class BookDetailSerializer(BookSerializer):
    # Замість просто ID автора, підставляємо повну інформацію про нього
    author = AuthorSerializer(read_only=True)
    total_borrowings = serializers.SerializerMethodField()

    class Meta(BookSerializer.Meta):
        fields = BookSerializer.Meta.fields + ['total_borrowings']

    def get_total_borrowings(self, obj):
        return obj.borrowings.count()