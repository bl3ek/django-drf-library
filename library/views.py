from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from .models import Author, Book, Borrowing
from .serializers import AuthorSerializer, BookSerializer, BorrowingSerializer, BookDetailSerializer
from .permissions import IsAdminOrReadOnly, IsBorrowerOrAdmin

@extend_schema(responses=AuthorSerializer(many=True), tags=['v1'])
@api_view(['GET'])
def author_list(request):
    authors = Author.objects.all()
    serializer = AuthorSerializer(authors, many=True)
    return Response({
        "count": authors.count(),
        "data": serializer.data
    })

@extend_schema(responses=AuthorSerializer, tags=['v1'])
@api_view(['GET'])
def author_detail(request, pk):
    author = get_object_or_404(Author, pk=pk)
    serializer = AuthorSerializer(author)
    return Response(serializer.data)

@extend_schema(responses=BookSerializer(many=True), tags=['v1'])
@api_view(['GET'])
def book_list(request):
    books = Book.objects.all()
    serializer = BookSerializer(books, many=True)
    return Response({
        "count": books.count(),
        "data": serializer.data
    })

@extend_schema(responses=BookDetailSerializer, tags=['v1'])
@api_view(['GET'])
def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    serializer = BookDetailSerializer(book)
    return Response(serializer.data)

@extend_schema(responses=BorrowingSerializer(many=True), tags=['v1'])
@api_view(['GET'])
def borrowing_list(request):
    borrowings = Borrowing.objects.all()
    serializer = BorrowingSerializer(borrowings, many=True)
    return Response({
        "count": borrowings.count(),
        "data": serializer.data
    })

@extend_schema(responses=BookSerializer(many=True), tags=['v1'])
@api_view(['GET'])
def available_books(request):
    books = Book.objects.filter(available_copies__gt=0)
    serializer = BookSerializer(books, many=True)
    return Response({
        "count": books.count(),
        "data": serializer.data
    })

@extend_schema(tags=['Authors'])
class AuthorListCreateAPIView(generics.ListCreateAPIView):
    """Отримання списку авторів або створення нового автора"""
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAdminOrReadOnly]

@extend_schema(tags=['Authors'])
class AuthorDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Перегляд, зміна або видалення конкретного автора"""
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAdminOrReadOnly]
    lookup_url_kwarg = 'author_id'

@extend_schema(tags=['Books'])
class BookListCreateAPIView(generics.ListCreateAPIView):
    """Отримання списку книг або додавання нової книги"""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminOrReadOnly]

@extend_schema(tags=['Books'])
class BookDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Перегляд, редагування або видалення конкретної книги"""
    queryset = Book.objects.all()
    serializer_class = BookDetailSerializer
    permission_classes = [IsAdminOrReadOnly]

@extend_schema(
    summary="Отримати список доступних книг",
    description="Повертає список книг, які є в наявності (кількість копій > 0)",
    tags=['Books']
)
class AvailableBookListAPIView(generics.ListAPIView):
    serializer_class = BookSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        return Book.objects.filter(available_copies__gt=0)

@extend_schema(tags=['Borrowings'])
class BorrowingListCreateAPIView(generics.ListCreateAPIView):
    """Отримання історії позик або створення нового запису позики"""
    serializer_class = BorrowingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Borrowing.objects.all()
        return Borrowing.objects.filter(reader=self.request.user)

    def perform_create(self, serializer):
        serializer.save(reader=self.request.user)

@extend_schema(tags=['Borrowings'])
class BorrowingDetailAPIView(generics.RetrieveUpdateAPIView):
    """Перегляд деталей конкретної позики або оновлення дати повернення"""
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer
    permission_classes = [IsAuthenticated, IsBorrowerOrAdmin]