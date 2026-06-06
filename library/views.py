from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Author, Book, Borrowing
from .serializers import AuthorSerializer, BookSerializer, BorrowingSerializer, BookDetailSerializer

# 1. Список усіх авторів
@api_view(['GET'])
def author_list(request):
    authors = Author.objects.all()
    serializer = AuthorSerializer(authors, many=True)
    return Response({
        "count": authors.count(),
        "data": serializer.data
    })

# 2. Деталі одного автора за ID
@api_view(['GET'])
def author_detail(request, pk):
    author = get_object_or_404(Author, pk=pk)
    serializer = AuthorSerializer(author)
    return Response(serializer.data)

# 3. Список усіх книг
@api_view(['GET'])
def book_list(request):
    books = Book.objects.all()
    serializer = BookSerializer(books, many=True)
    return Response({
        "count": books.count(),
        "data": serializer.data
    })

# 4. Деталі однієї книги за ID (використовуємо наш бонусний детальний серіалізатор)
@api_view(['GET'])
def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    serializer = BookDetailSerializer(book)
    return Response(serializer.data)

# 5. Список усіх позик
@api_view(['GET'])
def borrowing_list(request):
    borrowings = Borrowing.objects.all()
    serializer = BorrowingSerializer(borrowings, many=True)
    return Response({
        "count": borrowings.count(),
        "data": serializer.data
    })

# 6. Список лише доступних книг (де доступних копій більше 0)
@api_view(['GET'])
def available_books(request):
    books = Book.objects.filter(available_copies__gt=0)
    serializer = BookSerializer(books, many=True)
    return Response({
        "count": books.count(),
        "data": serializer.data
    })