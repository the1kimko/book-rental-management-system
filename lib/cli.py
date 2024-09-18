import click
from models import User, Book, Rental, Session
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timezone, timedelta


@click.group()
def cli():
    """Main entry point for the CLI."""
    pass

# ============ User Management ============

@click.command()
@click.argument('name')
@click.argument('email')
def add_user(name, email):
    """Add a new user to the system"""
    session = Session()
    try:
        if not name or not email:
            raise ValueError("Both name and email are required.")
        user = User(name=name, email=email)
        session.add(user)
        session.commit()
        click.echo(f"User '{name}' added successfully with ID: {user.id}")
    except IntegrityError:
        session.rollback()
        click.echo("Error: Email already exists in the system.")
    except ValueError as e:
        click.echo(str(e))
    finally:
        session.close()

@click.command()
@click.argument('user_id', type=int)
def delete_user(user_id):
    """Delete a user by their ID"""
    session = Session()
    try:
        user = session.get(User, user_id)
        if not user:
            click.echo(f"Error: User with ID {user_id} does not exist.")
        else:
            session.delete(user)
            session.commit()
            click.echo(f"User ID {user_id} successfully deleted.")
    except Exception as e:
        session.rollback()
        click.echo(f"Error: {str(e)}")
    finally:
        session.close()

@click.command()
def list_users():
    """List all users in the system"""
    session = Session()
    users = session.query(User).all()
    session.close()
    if users:
        for user in users:
            click.echo(f"User ID: {user.id}, Name: {user.name}, Email: {user.email}")
    else:
        click.echo("No active users.")

# ============ Book Management ============

@click.command()
@click.argument('title')
@click.argument('author')
@click.option('--available', default=1, help="Number of available copies")
def add_book(title, author, available):
    """Add a new book to the system with an optional available copies argument"""
    session = Session()
    try:
        if not title or not author:
            raise ValueError("Both title and author are required.")
        if available <= 0:
            raise ValueError("Available copies must be at least 1.")
        
        # Create a new book with the specified availability
        book = Book(title=title, author=author, available=available)
        session.add(book)
        session.commit()
        
        click.echo(f"Book '{title}' by '{author}' added successfully with ID: {book.id}")
    except ValueError as e:
        click.echo(str(e))
    finally:
        session.close()

@click.command()
@click.argument('book_id', type=int)
def delete_book(book_id):
    """Delete a book by its ID"""
    session = Session()
    try:
        book = session.get(Book, book_id)
        if not book:
            click.echo(f"Error: Book with ID {book_id} does not exist.")
        else:
            session.delete(book)
            session.commit()
            click.echo(f"Book ID {book_id} successfully deleted.")
    except Exception as e:
        session.rollback()
        click.echo(f"Error: {str(e)}")
    finally:
        session.close()

@click.command()
def list_books():
    """List all available books"""
    session = Session()
    books = session.query(Book).filter(Book.available > 0).all()
    session.close()
    if books:
        for book in books:
            click.echo(f"Book ID: {book.id}, Title: {book.title}, Author: {book.author}")
    else:
        click.echo("No available books.")

@click.command()
@click.option('--title', default=None, help="Filter books by title.")
@click.option('--author', default=None, help="Filter books by author.")
def search_books(title, author):
    """Search for books by title and/or author"""
    session = Session()
    try:
        query = session.query(Book).filter(Book.available > 0)
        if title:
            query = query.filter(Book.title.ilike(f'%{title}%'))
        if author:
            query = query.filter(Book.author.ilike(f'%{author}%'))

        books = query.all()
        session.close()
        if books:
            for book in books:
                click.echo(f"Book ID: {book.id}, Title: {book.title}, Author: {book.author}")
        else:
            click.echo("No matching books found.")
    except ValueError as e:
        click.echo(str(e))
    finally:
        session.close()

# ============ Rental Management ============

@click.command()
@click.argument('user_id', type=int)
@click.argument('book_id', type=int)
def rent_book(user_id, book_id):
    """Rent a book by adding a row to the `Rentals` table and updating the `user_books` association."""
    session = Session()
    try:
        user = session.get(User, user_id)
        book = session.get(Book, book_id)

        if not user:
            click.echo("Error: User not found.")
            return
        if not book:
            click.echo("Error: Book not found.")
            return
        if book.available <= 0:
            click.echo("Error: Book is unavailable.")
            return

        # Add a new rental record
        rental = Rental(user_id=user_id, book_id=book_id, rent_date=datetime.now(timezone.utc), due_date=datetime.now(timezone.utc) + timedelta(days=14))
        session.add(rental)

        # Update the user_books association table
        user.books.append(book)
        book.available -= 1

        session.commit()
        click.echo(f"User '{user.name}' rented book '{book.title}'")
    except Exception as e:
        session.rollback()
        click.echo(f"Error: {str(e)}")
    finally:
        session.close()

@click.command()
@click.argument('rental_id', type=int)
def return_book(rental_id):
    """Return a rented book by removing the association and calculating any penalties."""
    session = Session()
    try:
        rental = session.get(Rental, rental_id)
        if not rental or rental.return_date:
            click.echo("Error: Rental either doesn't exist or the book has already been returned.")
            return
        
        rental.return_date = datetime.utcnow()
        rental.calculate_penalty()

        book = session.query(Book).get(rental.book_id)
        book.available += 1

        session.commit()
        click.echo(f"Rental ID {rental_id} successfully returned with a penalty of {rental.penalty} KSh.")
    except Exception as e:
        session.rollback()
        click.echo(f"Error: {str(e)}")
    finally:
        session.close()

@click.command()
@click.argument('rental_id', type=int)
def calculate_penalty(rental_id):
    """Calculate penalty for a rental"""
    session = Session()
    try:
        rental = session.get(Rental, rental_id)
        if rental.return_date and rental.return_date > rental.due_date:
            days_late = (rental.return_date - rental.due_date).days
            penalty_amount = days_late * 50  # KSh 50 per day late
            click.echo(f"Penalty for Rental ID {rental_id}: {penalty_amount} KSh")
        else:
            click.echo(f"No penalty for Rental ID {rental_id}.")
    finally:
        session.close()

@click.command()
def list_rentals():
    """List all active rentals"""
    session = Session()
    try:
        rentals = session.query(Rental).filter(Rental.return_date == None).all()
        
        if rentals:
            for rental in rentals:
                click.echo(f"Rental ID: {rental.id}, User ID: {rental.user_id}, Book: {rental.book.title}")
        else:
            click.echo("No active rentals.")

    except Exception as e:
        click.echo(f"Error: {str(e)}")

    finally:
        session.close()

# ============ Add commands to CLI group ============

cli.add_command(add_user)
cli.add_command(delete_user)
cli.add_command(list_users)

cli.add_command(add_book)
cli.add_command(delete_book)
cli.add_command(list_books)
cli.add_command(search_books)

cli.add_command(rent_book)
cli.add_command(return_book)
cli.add_command(calculate_penalty)
cli.add_command(list_rentals)

if __name__ == '__main__':
    cli()
