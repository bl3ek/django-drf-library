from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework import generics
from .models import Author, Book, Borrowing
from .serializers import AuthorSerializer, BookSerializer, BorrowingSerializer, BookDetailSerializer

@api_view(['GET'])
def author_list(request):
    authors = Author.objects.all()
    serializer = AuthorSerializer(authors, many=True)
    return Response({
        "count": authors.count(),
        "data": serializer.data
    })

@api_view(['GET'])
def author_detail(request, pk):
    author = get_object_or_404(Author, pk=pk)
    serializer = AuthorSerializer(author)
    return Response(serializer.data)

@api_view(['GET'])
def book_list(request):
    books = Book.objects.all()
    serializer = BookSerializer(books, many=True)
    return Response({
        "count": books.count(),
        "data": serializer.data
    })

@api_view(['GET'])
def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    serializer = BookDetailSerializer(book)
    return Response(serializer.data)

@api_view(['GET'])
def borrowing_list(request):
    borrowings = Borrowing.objects.all()
    serializer = BorrowingSerializer(borrowings, many=True)
    return Response({
        "count": borrowings.count(),
        "data": serializer.data
    })

@api_view(['GET'])
def available_books(request):
    books = Book.objects.filter(available_copies__gt=0)
    serializer = BookSerializer(books, many=True)
    return Response({
        "count": books.count(),
        "data": serializer.data
    })

class AuthorListCreateAPIView(generics.ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class AuthorDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    lookup_url_kwarg = 'author_id'

class BookListCreateAPIView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookDetailSerializer

class AvailableBookListAPIView(generics.ListAPIView):
    serializer_class = BookSerializer

    def get_queryset(self):
        return Book.objects.filter(available_copies__gt=0)

class BorrowingListCreateAPIView(generics.ListCreateAPIView):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer