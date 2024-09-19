import click
from lib.services.user_service import UserService
from lib.services.book_service import BookService
from lib.services.rental_service import RentalService

user_service = UserService()
book_service = BookService()
rental_service = RentalService()


@click.group()
def cli():
    """Main entry point for the CLI."""
    pass

# User management
@click.command()
@click.argument('name')
@click.argument('email')
def add_user(name, email):
    result = user_service.add_user(name, email)
    click.echo(result)

@click.command()
@click.argument('user_id', type=int)
def delete_user(user_id):
    result = user_service.delete_user(user_id)
    click.echo(result)

@click.command()
def list_users():
    users = user_service.list_users()
    for user in users:
        click.echo(user)

# Book management
@click.command()
@click.argument('title')
@click.argument('author')
@click.option('--available', default=1)
@click.option('--genres', default=None)
def add_book(title, author, available, genres):
    result = book_service.add_book(title, author, available, genres)
    click.echo(result)

@click.command()
@click.argument('book_id', type=int)
def delete_book(book_id):
    result = book_service.delete_book(book_id)
    click.echo(result)

@click.command()
@click.option('--sort-by', type=click.Choice(['genre', 'author']), help="Sort books by genre or author.")
def list_books(sort_by):
    """List all books and allow sorting by genre or author."""
    books = book_service.list_books(sort_by)
    for book in books:
        click.echo(book)


@click.command()
@click.option('--title', default=None, help="Filter books by title.")
@click.option('--author', default=None, help="Filter books by author.")
def search_books(title, author):
    """Search for books by title and/or author."""
    
    # Instantiate BookService inside the function
    book_service = BookService()
    
    # Use the service to search books
    books = book_service.search_books(title, author)
    
    if isinstance(books, str):  # Handle any error messages returned from the service
        click.echo(f"Error: {books}")
    elif books:
        for book in books:
            click.echo(f"Book ID: {book.id}, Title: {book.title}, Author: {book.author}")
    else:
        click.echo("No matching books found.")

# Rental management
@click.command()
@click.argument('user_id', type=int)
@click.argument('book_id', type=int)
def rent_book(user_id, book_id):
    result = rental_service.rent_book(user_id, book_id)
    click.echo(result)

@click.command()
@click.argument('rental_id', type=int)
def return_book(rental_id):
    result = rental_service.return_book(rental_id)
    click.echo(result)

@click.command()
def list_rentals():
    """List all rentals, with returned ones sorted by return date"""
    rentals = rental_service.list_rentals()
    for rental in rentals:
        click.echo(rental)

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
cli.add_command(list_rentals)

if __name__ == '__main__':
    cli()
