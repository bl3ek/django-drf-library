from django.core.management.base import BaseCommand
from library.models import Reader, Author, Book, Borrowing
from datetime import date

class Command(BaseCommand):
    help = 'Заповнює базу даних тестовими даними для бібліотеки'

    def handle(self, *args, **kwargs):
        self.stdout.write('Очищення старої бази даних...')
        Borrowing.objects.all().delete()
        Book.objects.all().delete()
        Author.objects.all().delete()
        Reader.objects.all().delete()

        self.stdout.write('Створення читачів (користувачів)...')
        reader1 = Reader.objects.create_user(username='ivan_reader', password='password123', phone='+380991112233', address='Київ')
        reader2 = Reader.objects.create_user(username='olena_reader', password='password123', phone='+380674445566', address='Львів')

        self.stdout.write('Створення 5 авторів...')
        authors = []
        for i in range(1, 6):
            author = Author.objects.create(
                name=f'Автор Номер {i}',
                bio=f'Це дивовижна біографія видатного автора під номером {i}.',
                birth_date=date(1960 + i * 2, i, i)
            )
            authors.append(author)

        self.stdout.write('Створення 10 книг...')
        books = []
        for i in range(1, 11):
            # Робимо так, щоб у деяких книг було 0 доступних копій для перевірки фільтрації
            copies = 0 if i in [3, 7] else i % 4 + 1
            
            book = Book.objects.create(
                title=f'Цікава Книга {i}',
                author=authors[i % 5],
                description=f'Опис сюжету та проблематики бестселера {i}.',
                isbn=f'978123456789{i-1}',  # Рівно 13 символів
                published_date=date(2015 + i % 3, 5, i),
                pages=100 + i * 25,
                available_copies=copies
            )
            books.append(book)

        self.stdout.write('Створення 5 позик...')
        for i in range(5):
            Borrowing.objects.create(
                book=books[i],
                reader=reader1 if i % 2 == 0 else reader2,
                is_returned=i % 3 == 0,
                return_date=date.today() if i % 3 == 0 else None
            )

        self.stdout.write(self.style.SUCCESS('Базу даних успішно заповнено тестовими даними!'))