from lib.models import Session, User, Book, Rental
from datetime import datetime, timezone, timedelta
from sqlalchemy.exc import IntegrityError

# Function to populate the database with seed data
def seed_data():
    session = Session()

    # Seed Users
    users = [
        User(name="John Doe", email="john@example.com"),
        User(name="Jane Smith", email="jane@example.com"),
        User(name="Alice Johnson", email="alice@example.com"),
        User(name="Kimu Lami", email="lamiku@yahoo.com"),
    ]
    
    # Seed Books with Genre
    books = [
        Book(title="1984", author="George Orwell", genres="Dystopian", available=5),
        Book(title="To Kill a Mockingbird", author="Harper Lee", genres="Fiction", available=3),
        Book(title="The Great Gatsby", author="F. Scott Fitzgerald", genres="Classics", available=4),
        Book(title="The Hitchhiker's Guide to the Galaxy", author="Douglas Adams", genres="Non-Fictional", available=2),
        Book(title="Brave New World", author="Aldous Huxley", genres="Dystopian", available=5),
        Book(title="Sinners", author="Susan Haluwa", genres="African Fiction", available=7)
    ]

    # Add Users to the database
    for user in users:
        try:
            # Check if the user already exists by email
            existing_user = session.query(User).filter_by(email=user.email).first()
            if existing_user:
                print(f"User with email {user.email} already exists.")
            else:
                session.add(user)
                session.commit()
                print(f"User {user.name} added successfully.")
        except IntegrityError:
            session.rollback()  # Rollback the session in case of IntegrityError
            print(f"Error adding user {user.name}.")

    # Add Books to the database
    for book in books:
        try:
            # Check if the book already exists by title and author
            existing_book = session.query(Book).filter_by(title=book.title, author=book.author).first()
            if existing_book:
                print(f"Book '{book.title}' by {book.author} already exists.")
            else:
                session.add(book)
                session.commit()
                print(f"Book '{book.title}' by {book.author} added successfully.")
        except IntegrityError:
            session.rollback()  # Rollback the session in case of IntegrityError
            print(f"Error adding book '{book.title}' by {book.author}.")

    # Rent books to users to populate the user_books join table
    rent_book_for_seed(session, "John Doe", "1984", days_rented_ago=20, due_days_ago=10)
    rent_book_for_seed(session, "Jane Smith", "To Kill a Mockingbird", days_rented_ago=7, due_days_ago=10)
    rent_book_for_seed(session, "Alice Johnson", "The Great Gatsby")
    rent_book_for_seed(session, "Kimu Lami", "Sinners", days_rented_ago=14, due_days_ago=10)  # Simulates a late return

    # Close the session after all operations are complete
    session.close()
    print("Database has been seeded successfully!")

# Function to create a rental and update the user_books join table (for seed data)
def rent_book_for_seed(session, user_name, book_title, days_rented_ago=0, due_days_ago=0):
    user = session.query(User).filter_by(name=user_name).first()
    book = session.query(Book).filter_by(title=book_title).first()

    if user and book:
        # Check if the user has already rented this book (i.e., if there's an active rental for the same book)
        existing_rental = session.query(Rental).filter_by(user_id=user.id, book_id=book.id, return_date=None).first()
        
        if existing_rental:
            print(f"User '{user.name}' has already rented '{book.title}'.")
        elif book.available <= 0:
            print(f"Book '{book.title}' is unavailable.")
        else:
            try:
                # Create a rental with the option to simulate late return and penalties
                rent_date = datetime.now(timezone.utc) - timedelta(days=days_rented_ago)
                due_date = datetime.now(timezone.utc) - timedelta(days=due_days_ago) if due_days_ago > 0 else None

                # Create a rental
                rental = Rental(user_id=user.id, book_id=book.id, rent_date=rent_date, due_date=due_date)
                
                # Append the book to the user's books collection (this updates the user_books join table)
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
                    print(f"Book '{book.title}' rented by {user.name} with a penalty due to late return.")
                else:
                    print(f"Book '{book.title}' rented by {user.name}.")
            except IntegrityError:
                session.rollback()
                print(f"Failed to rent '{book.title}' to {user.name}.")
    else:
        if not user:
            print(f"User '{user_name}' not found.")
        if not book:
            print(f"Book '{book_title}' not found.")

if __name__ == "__main__":
    seed_data()
