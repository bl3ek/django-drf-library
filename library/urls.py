from django.urls import path
from . import views

app_name = 'library'

urlpatterns = [
    path('v1/authors/', views.author_list, name='v1_author_list'),
    path('v1/authors/<int:pk>/', views.author_detail, name='v1_author_detail'),
    path('v1/books/', views.book_list, name='v1_book_list'),
    path('v1/books/<int:pk>/', views.book_detail, name='v1_book_detail'),
    path('v1/borrowings/', views.borrowing_list, name='v1_borrowing_list'),
    path('v1/books/available/', views.available_books, name='v1_available_books'),

    path('v2/authors/', views.AuthorListCreateAPIView.as_view(), name='v2_author_list_create'),
    path('v2/authors/<int:author_id>/', views.AuthorDetailAPIView.as_view(), name='v2_author_detail'),
    path('v2/books/', views.BookListCreateAPIView.as_view(), name='v2_book_list_create'),
    path('v2/books/<int:pk>/', views.BookDetailAPIView.as_view(), name='v2_book_detail'),
    path('v2/books/available/', views.AvailableBookListAPIView.as_view(), name='v2_available_books'),
    path('v2/borrowings/', views.BorrowingListCreateAPIView.as_view(), name='v2_borrowing_list_create'),
    path('v2/borrowings/<int:pk>/', views.BorrowingDetailAPIView.as_view(), name='v2_borrowing_detail'),
]