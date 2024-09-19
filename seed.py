from sqlalchemy.exc import IntegrityError
from lib.services.user_service import UserService
from lib.services.book_service import BookService
from lib.services.rental_service import RentalService
from lib.models import User, Book, Rental, UserBook
from lib.database import get_session
from datetime import datetime, timezone, timedelta

# Initialize services
user_service = UserService()
book_service = BookService()
rental_service = RentalService()

def clear_database():
    """Delete all rows from all tables."""
    session = get_session()
    try:
        session.query(UserBook).delete()
        session.query(Rental).delete()
        session.query(Book).delete()
        session.query(User).delete()
        session.commit()
        print("All data cleared from the database.")
    except Exception as e:
        session.rollback()
        print(f"Error clearing database: {str(e)}")
    finally:
        session.close()

# Function to populate the database with seed data
def seed_data():
    # First, clear the database
    clear_database()

    # Seed Users
    users = [
        {"name": "John Doe", "email": "john@example.com"},
        {"name": "Jane Smith", "email": "jane@example.com"},
        {"name": "Alice Johnson", "email": "alice@example.com"},
        {"name": "Kimu Lami", "email": "lamiku@yahoo.com"},
        {"name": "Bruce Wayne", "email": "bruce@wayne.com"},
        {"name": "Clark Kent", "email": "clark@dailyplanet.com"},
        {"name": "Peter Parker", "email": "peter@bugle.com"},
        {"name": "Tony Stark", "email": "tony@starkindustries.com"},
        {"name": "Natasha Romanoff", "email": "natasha@avengers.com"},
        {"name": "Wanda Maximoff", "email": "wanda@avengers.com"}
    ]

    # Seed Books with Genre
    books = [
        {"title": "1984", "author": "George Orwell", "genres": "Dystopian", "available": 5},
        {"title": "To Kill a Mockingbird", "author": "Harper Lee", "genres": "Fiction", "available": 3},
        {"title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "genres": "Classics", "available": 4},
        {"title": "The Hitchhiker's Guide to the Galaxy", "author": "Douglas Adams", "genres": "Non-Fictional", "available": 2},
        {"title": "Brave New World", "author": "Aldous Huxley", "genres": "Dystopian", "available": 5},
        {"title": "Sinners", "author": "Susan Haluwa", "genres": "African Fiction", "available": 7},
        {"title": "Harry Potter and the Philosopher's Stone", "author": "J.K. Rowling", "genres": "Fantasy", "available": 6},
        {"title": "The Hobbit", "author": "J.R.R. Tolkien", "genres": "Fantasy", "available": 8},
        {"title": "Moby Dick", "author": "Herman Melville", "genres": "Adventure", "available": 5},
        {"title": "War and Peace", "author": "Leo Tolstoy", "genres": "Historical Fiction", "available": 3}
    ]

    # Add Users to the database
    for user in users:
        result = user_service.add_user(user['name'], user['email'])
        print(result)

    # Add Books to the database
    for book in books:
        result = book_service.add_book(book['title'], book['author'], book['available'], book['genres'])
        print(result)

    # Seed Rentals
    rentals = [
        {"user_name": "John Doe", "book_title": "1984", "days_rented_ago": 20, "due_days_ago": 10},  # Late return
        {"user_name": "Jane Smith", "book_title": "To Kill a Mockingbird", "days_rented_ago": 7},      # On time
        {"user_name": "Alice Johnson", "book_title": "The Great Gatsby", "days_rented_ago": 3},        # On time
        {"user_name": "Kimu Lami", "book_title": "Sinners", "days_rented_ago": 14, "due_days_ago": 5},  # Late return
    ]

    for rental in rentals:
        rent_book_for_seed(
            rental['user_name'],
            rental['book_title'],
            rental.get('days_rented_ago', 0),
            rental.get('due_days_ago', 0)
        )

    print("Database has been seeded successfully!")

# Function to create a rental and update the user_books join table (for seed data)
def rent_book_for_seed(user_name, book_title, days_rented_ago=0, due_days_ago=0):
    session = get_session()
    try:
        user = session.query(User).filter_by(name=user_name).first()
        book = session.query(Book).filter_by(title=book_title).first()

        if not user:
            print(f"Error: User '{user_name}' not found.")
            return
        if not book:
            print(f"Error: Book '{book_title}' not found.")
            return
        if book.available <= 0:
            print(f"Error: Book '{book_title}' is unavailable.")
            return

        # Create a rental with the option to simulate late return and penalties
        rent_date = datetime.now(timezone.utc) - timedelta(days=days_rented_ago)
        due_date = rent_date + timedelta(days=14) if due_days_ago == 0 else datetime.now(timezone.utc) - timedelta(days=due_days_ago)

        # Create a rental
        rental = Rental(user_id=user.id, book_id=book.id, rent_date=rent_date, due_date=due_date)

        # **APPEND the book to the user's books collection (updates user_books)**
        user.books.append(book)

        # Reduce the available copies of the book
        book.available -= 1

        # If the book is overdue, simulate return and calculate penalty
        if due_days_ago > 0:
            rental.return_date = datetime.now(timezone.utc)  # Simulate the return
            rental.calculate_penalty()  # Assuming this method calculates late fees based on the due date

        # Commit the changes
        session.add(rental)
        session.commit()

        if due_days_ago > 0:
            print(f"Book '{book.title}' rented by {user.name} with a penalty for late return.")
        else:
            print(f"Book '{book.title}' rented by {user.name}.")

    except IntegrityError:
        session.rollback()
        print(f"Failed to rent '{book.title}' to {user.name}.")
    finally:
        session.close()

if __name__ == "__main__":
    seed_data()
