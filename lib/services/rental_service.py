from sqlalchemy.orm import joinedload
from lib.models import Rental, Book, User
from datetime import datetime, timedelta, timezone
from lib.database import get_session

class RentalService:
    def rent_book(self, user_id, book_id):
        """Rent a book"""
        session = get_session()
        try:
            user = session.get(User, user_id)
            book = session.get(Book, book_id)

            if not user:
                return "Error: User not found."
            if not book:
                return "Error: Book not found."
            if book.available <= 0:
                return "Error: Book is unavailable."
            
            # Check if the user already has an active rental for this book
            active_rental = session.query(Rental).filter_by(user_id=user_id, book_id=book_id, return_date=None).first()
            if active_rental:
                return f"Error: User '{user.name}' has already rented '{book.title}' and hasn't returned it yet."

            rental = Rental(
                user_id=user_id,
                book_id=book_id,
                rent_date=datetime.now(timezone.utc),
                due_date=datetime.now(timezone.utc) + timedelta(days=14)
            )
            # Update the user_books association table
            user.books.append(book)
            book.available -= 1
            
            session.add(rental)
            session.commit()
            return f"User '{user.name}' rented book '{book.title}'"
        except Exception as e:
            self.session.rollback()
            raise e
        finally:
            session.close()

    def return_book(self, rental_id):
        """Return a book and calculate any penalties"""
        session = get_session()
        try:
            rental = session.get(Rental, rental_id)
            if not rental or rental.return_date:
                return "Error: Rental either doesn't exist or the book has already been returned."
            
            rental.return_date = datetime.now(timezone.utc)
            rental.calculate_penalty()

            book = session.get(Book, rental.book_id)
            book.available += 1
            session.commit()
            return f"Rental ID {rental_id} returned with a penalty of {rental.penalty} KSh."
        finally:
            session.close()

    def list_rentals(self):
        """List all rentals, sorting returned ones"""
        session = get_session()
        try:
            # Use joinedload to eagerly load the 'book' relationship
            rentals = session.query(Rental).options(joinedload(Rental.book)).all()

            # Separate returned and active rentals
            returned_rentals = [rental for rental in rentals if rental.return_date is not None]
            active_rentals = [rental for rental in rentals if rental.return_date is None]

            # Sort returned rentals by return_date (oldest to newest)
            returned_rentals_sorted = sorted(returned_rentals, key=lambda r: r.return_date)

            # Prepare the result for display
            result = []

            # First, display active rentals
            result.append("Active Rentals:")
            for rental in active_rentals:
                result.append(f"Rental ID: {rental.id}, User ID: {rental.user_id}, Book: {rental.book.title}")

            # Then, display returned rentals (sorted)
            result.append("\nReturned Rentals (sorted by return date):")
            for rental in returned_rentals_sorted:
                result.append(f"Rental ID: {rental.id}, User ID: {rental.user_id}, Book: {rental.book.title}, Returned on: {rental.return_date}")

            return result
        finally:
            session.close()
    
    def rent_book_by_name(self, user_name, book_title, days_rented_ago=0, due_days_ago=0):
        """Rent a book by user name and book title (for seed data purposes)"""
        session = get_session()
        try:
            user = session.query(User).filter_by(name=user_name).first()
            book = session.query(Book).filter_by(title=book_title).first()

            if not user:
                return f"Error: User '{user_name}' not found."
            if not book:
                return f"Error: Book '{book_title}' not found."
            if book.available <= 0:
                return f"Error: Book '{book_title}' is unavailable."

            # Create the rental
            rent_date = datetime.now(timezone.utc) - timedelta(days=days_rented_ago)
            due_date = datetime.now(timezone.utc) - timedelta(days=due_days_ago) if due_days_ago > 0 else rent_date + timedelta(days=14)

            rental = Rental(user_id=user.id, book_id=book.id, rent_date=rent_date, due_date=due_date)
            session.add(rental)
            book.available -= 1

            # If the book is overdue, simulate the return and calculate penalty
            if due_days_ago > 0:
                rental.return_date = datetime.now(timezone.utc)  # Simulate return
                rental.calculate_penalty()

            session.commit()

            if due_days_ago > 0:
                return f"Book '{book.title}' rented by {user.name} with a penalty for late return."
            else:
                return f"Book '{book.title}' rented by {user.name}."
        except Exception as e:
            session.rollback()
            return f"Error renting book: {str(e)}"
        finally:
            session.close()
