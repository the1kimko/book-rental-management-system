from lib.models import Book
from lib.database import get_session

class BookService:
    def add_book(self, title, author, available, genres=None):
        """Add a new book to the system"""
        session = get_session()
        try:
            if not title or not author:
                raise ValueError("Title and author are required.")
            if available <= 0:
                raise ValueError("Available copies must be at least 1.")
            
            book = Book(title=title, author=author, available=available, genres=genres)
            session.add(book)
            session.commit()
            return f"Book '{title}' by '{author}' added successfully with ID: {book.id}"
        except ValueError as e:
            return str(e)
        finally:
            session.close()

    def delete_book(self, book_id):
        """Delete a book by its ID"""
        session = get_session()
        try:
            book = session.get(Book, book_id)
            if not book:
                return f"Error: Book with ID {book_id} does not exist."
            session.delete(book)
            session.commit()
            return f"Book ID {book_id} successfully deleted."
        finally:
            session.close()

    def list_books(self, sort_by=None):
        """List all books and allow sorting by genre or author"""
        session = get_session()
        query = session.query(Book).filter(Book.available > 0)
        
        if sort_by == "genre":
            query = query.order_by(Book.genres)
        elif sort_by == "author":
            query = query.order_by(Book.author)

        books = query.all()
        session.close()
        return [f"Book ID: {book.id}, Title: {book.title}, Author: {book.author}, Genre: {book.genres}" for book in books]
    
    def search_books(self, title=None, author=None):
        """Search for books by title and/or author."""
        session = get_session()
        try:
            query = session.query(Book).filter(Book.available > 0)  # Only search available books

            # Filter by title if provided
            if title:
                query = query.filter(Book.title.ilike(f'%{title}%'))
            
            # Filter by author if provided
            if author:
                query = query.filter(Book.author.ilike(f'%{author}%'))
            
            books = query.all()
            session.close()

            return books  # Return the list of books

        except Exception as e:
            session.rollback()  # Rollback in case of an error
            return str(e)
        finally:
            session.close()