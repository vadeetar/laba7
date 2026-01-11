Python
                         Копировать
                    from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
                    from sqlalchemy.ext.declarative import declarative_base
                    from sqlalchemy.orm import sessionmaker, relationship
                    from sqlalchemy.sql import func
                    from datetime import datetime

                    # 1. Создаем базовый класс для моделей
                    Base = declarative_base()

                    # 2. Определяем модели (таблицы)
                    class Author(Base):
                    """Модель автора"""
                    __tablename__ = 'authors'

                    id = Column(Integer, primary_key=True)
                    name = Column(String(100), nullable=False)
                    birth_year = Column(Integer)
                    country = Column(String(50))
                    created_at = Column(DateTime, default=datetime.now)

                    # Связь один-ко-многим с книгами
                    books = relationship("Book", back_populates="author", cascade="all, delete-orphan")

                    def __repr__(self):
                    return f"
                        "

                        def to_dict(self):
                        return {
                        'id': self.id,
                        'name': self.name,
                        'birth_year': self.birth_year,
                        'country': self.country,
                        'book_count': len(self.books)
                        }

                        class Book(Base):
                        """Модель книги"""
                        __tablename__ = 'books'

                        id = Column(Integer, primary_key=True)
                        title = Column(String(200), nullable=False)
                        author_id = Column(Integer, ForeignKey('authors.id'), nullable=False)
                        year = Column(Integer)
                        pages = Column(Integer)
                        price = Column(Float)
                        created_at = Column(DateTime, default=datetime.now)
                        updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

                        # Связь многие-к-одному с автором
                        author = relationship("Author", back_populates="books")

                        # Связь многие-ко-многим с жанрами
                        genres = relationship("Genre", secondary="book_genres", back_populates="books")

                        def __repr__(self):
                        return f"
                            "

                            def to_dict(self):
                            return {
                            'id': self.id,
                            'title': self.title,
                            'author': self.author.name if self.author else None,
                            'year': self.year,
                            'pages': self.pages,
                            'price': self.price,
                            'genres': [genre.name for genre in self.genres]
                            }

                            class Genre(Base):
                            """Модель жанра"""
                            __tablename__ = 'genres'

                            id = Column(Integer, primary_key=True)
                            name = Column(String(50), unique=True, nullable=False)

                            # Связь многие-ко-многим с книгами
                            books = relationship("Book", secondary="book_genres", back_populates="genres")

                            def __repr__(self):
                            return f"
                                "

                                # Таблица для связи многие-ко-многим
                                class BookGenre(Base):
                                __tablename__ = 'book_genres'

                                book_id = Column(Integer, ForeignKey('books.id'), primary_key=True)
                                genre_id = Column(Integer, ForeignKey('genres.id'), primary_key=True)

                                # 3. Создаем движок и сессию
                                engine = create_engine('sqlite:///library.db', echo=False)  # echo=True для отладки SQL
                                Base.metadata.create_all(engine)
                                Session = sessionmaker(bind=engine)

                                # 4. Класс для работы с базой данных
                                class LibraryManager:
                                """Менеджер библиотеки на SQLAlchemy"""

                                def __init__(self):
                                self.session = Session()

                                def add_author(self, name, birth_year=None, country=None):
                                """Добавление автора"""
                                author = Author(name=name, birth_year=birth_year, country=country)
                                self.session.add(author)
                                self.session.commit()
                                print(f"✅ Добавлен автор: {author}")
                                return author

                                def add_book(self, title, author_name, year=None, pages=None, price=None):
                                """Добавление книги"""
                                # Находим или создаем автора
                                author = self.session.query(Author).filter_by(name=author_name).first()
                                if not author:
                                author = self.add_author(author_name)

                                # Создаем книгу
                                book = Book(
                                title=title,
                                author=author,
                                year=year,
                                pages=pages,
                                price=price
                                )

                                self.session.add(book)
                                self.session.commit()
                                print(f"✅ Добавлена книга: {book}")
                                return book

                                def add_genre(self, name):
                                """Добавление жанра"""
                                genre = Genre(name=name)
                                self.session.add(genre)
                                self.session.commit()
                                return genre

                                def assign_genre_to_book(self, book_title, genre_name):
                                """Назначение жанра книге"""
                                book = self.session.query(Book).filter_by(title=book_title).first()
                                genre = self.session.query(Genre).filter_by(name=genre_name).first()

                                if book and genre:
                                if genre not in book.genres:
                                book.genres.append(genre)
                                self.session.commit()
                                print(f"✅ Жанр '{genre_name}' назначен книге '{book_title}'")

                                def get_all_books(self):
                                """Получение всех книг"""
                                return self.session.query(Book).all()

                                def get_books_by_author(self, author_name):
                                """Получение книг по автору"""
                                return self.session.query(Book).join(Author).filter(Author.name == author_name).all()

                                def search_books(self, keyword):
                                """Поиск книг по ключевому слову"""
                                return self.session.query(Book).filter(
                                Book.title.ilike(f"%{keyword}%")
                                ).all()

                                def update_book_price(self, book_id, new_price):
                                """Обновление цены книги"""
                                book = self.session.query(Book).get(book_id)
                                if book:
                                old_price = book.price
                                book.price = new_price
                                self.session.commit()
                                print(f"✅ Цена книги '{book.title}' обновлена: {old_price} → {new_price}")
                                return book
                                return None

                                def delete_book(self, book_id):
                                """Удаление книги"""
                                book = self.session.query(Book).get(book_id)
                                if book:
                                self.session.delete(book)
                                self.session.commit()
                                print(f"✅ Книга '{book.title}' удалена")
                                return True
                                return False

                                def get_library_statistics(self):
                                """Получение статистики библиотеки"""
                                stats = {
                                'total_authors': self.session.query(Author).count(),
                                'total_books': self.session.query(Book).count(),
                                'total_genres': self.session.query(Genre).count(),
                                'avg_book_price': self.session.query(func.avg(Book.price)).scalar() or 0,
                                'most_prolific_author': None
                                }

                                # Находим самого продуктивного автора
                                result = self.session.query(
                                Author.name,
                                func.count(Book.id).label('book_count')
                                ).join(Book).group_by(Author.id).order_by(func.count(Book.id).desc()).first()

                                if result:
                                stats['most_prolific_author'] = {
                                'name': result[0],
                                'book_count': result[1]
                                }

                                return stats

                                def close(self):
                                """Закрытие сессии"""
                                self.session.close()

                                # 5. Пример использования
                                if __name__ == "__main__":
                                print("=== SQLALCHEMY ORM ДЕМОНСТРАЦИЯ ===")

                                # Создаем менеджер
                                library = LibraryManager()

                                try:
                                # Добавляем авторов
                                print("\n1. Добавление авторов:")
                                author1 = library.add_author("Михаил Булгаков", 1891, "Россия")
                                author2 = library.add_author("Фёдор Достоевский", 1821, "Россия")
                                author3 = library.add_author("Лев Толстой", 1828, "Россия")

                                # Добавляем книги
                                print("\n2. Добавление книг:")
                                library.add_book("Мастер и Маргарита", "Михаил Булгаков", 1966, 384, 500.0)
                                library.add_book("Собачье сердце", "Михаил Булгаков", 1925, 192, 350.0)
                                library.add_book("Преступление и наказание", "Фёдор Достоевский", 1866, 672, 450.0)
                                library.add_book("Война и мир", "Лев Толстой", 1869, 1225, 800.0)

                                # Добавляем жанры
                                print("\n3. Добавление жанров:")
                                library.add_genre("Роман")
                                library.add_genre("Фантастика")
                                library.add_genre("Классика")
                                library.add_genre("Драма")

                                # Назначаем жанры книгам
                                print("\n4. Назначение жанров:")
                                library.assign_genre_to_book("Мастер и Маргарита", "Роман")
                                library.assign_genre_to_book("Мастер и Маргарита", "Фантастика")
                                library.assign_genre_to_book("Преступление и наказание", "Роман")
                                library.assign_genre_to_book("Преступление и наказание", "Драма")
                                library.assign_genre_to_book("Война и мир", "Роман")
                                library.assign_genre_to_book("Война и мир", "Классика")

                                # Получаем все книги
                                print("\n5. Все книги в библиотеке:")
                                books = library.get_all_books()
                                for book in books:
                                print(f"  - {book.title} ({book.author.name}) - {book.price} руб.")

                                # Поиск книг по автору
                                print("\n6. Книги Михаила Булгакова:")
                                bulgakov_books = library.get_books_by_author("Михаил Булгаков")
                                for book in bulgakov_books:
                                print(f"  - {book.title} ({book.year})")

                                # Обновление цены
                                print("\n7. Обновление цены:")
                                library.update_book_price(1, 550.0)

                                # Поиск книг
                                print("\n8. Поиск книг по слову 'мир':")
                                found_books = library.search_books("мир")
                                for book in found_books:
                                print(f"  - {book.title}")

                                # Статистика библиотеки
                                print("\n9. Статистика библиотеки:")
                                stats = library.get_library_statistics()
                                print(f"  Всего авторов: {stats['total_authors']}")
                                print(f"  Всего книг: {stats['total_books']}")
                                print(f"  Всего жанров: {stats['total_genres']}")
                                print(f"  Средняя цена книги: {stats['avg_book_price']:.2f} руб.")
                                if stats['most_prolific_author']:
                                author_info = stats['most_prolific_author']
                                print(f"  Самый продуктивный автор: {author_info['name']} ({author_info['book_count']} книг)")

                                finally:
                                # Закрываем соединение
                                library.close()
                                print("\n✅ Сессия закрыта")

                                # 6. Дополнительные возможности SQLAlchemy
                                # - Сложные запросы с join
                                # - Фильтрация и сортировка
                                # - Пагинация
                                # - Транзакции
                                # - События и хуки
                                # - Миграции схемы базы данных# Коммит Sun Jan 11 17:56:58 RTZ 2026
