# debug.py

from lib.services.user_service import UserService
from lib.services.book_service import BookService
from lib.services.rental_service import RentalService
import click

# Instantiate services
user_service = UserService()
book_service = BookService()
rental_service = RentalService()

def main_menu():
    """Displays the main menu options."""
    while True:
        click.echo("\n===== Welcome to Jamii Book Rental Management System =====")
        click.echo("\n===== Main Menu =====")
        click.echo("1. Manage Users")
        click.echo("2. Manage Books")
        click.echo("3. Manage Rentals")
        click.echo("4. Exit")

        choice = input("Please choose an option: ").strip()

        if choice == "1":
            manage_users()
        elif choice == "2":
            manage_books()
        elif choice == "3":
            manage_rentals()
        elif choice == "4":
            click.echo("Exiting the program. Goodbye!")
            break
        else:
            click.echo("Invalid option. Please choose again.")

# ============= User Management Menu =============

def manage_users():
    """Displays the user management menu."""
    while True:
        click.echo("\n===== User Management =====")
        click.echo("1. Add a new user")
        click.echo("2. Delete a user")
        click.echo("3. List all users")
        click.echo("4. Find user by attribute")
        click.echo("5. Back to Main Menu")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_user()
        elif choice == "2":
            delete_user()
        elif choice == "3":
            list_users()
        elif choice == "4":
            find_user_by_attribute()
        elif choice == "5":
            break
        else:
            click.echo("Invalid option. Please choose again.")

def add_user():
    """Prompt the user to add a new user."""
    name = input("Enter user name: ").strip()
    email = input("Enter user email: ").strip()
    
    result = user_service.add_user(name, email)
    click.echo(result)

def delete_user():
    """Prompt the user to delete a user by ID."""
    user_id = input("Enter user ID to delete: ").strip()
    
    result = user_service.delete_user(int(user_id))
    click.echo(result)

def list_users():
    """List all users."""
    users = user_service.list_users()
    if isinstance(users, list):
        click.echo("\nUsers:")
        for user in users:
            click.echo(user)
    else:
        click.echo(users)

def find_user_by_attribute():
    """Find a user by attribute."""
    click.echo("\nFind User By:")
    click.echo("1. Name")
    click.echo("2. Email")

    choice = input("Choose an option: ").strip()
    query = input("Enter the value to search for: ").strip()
    
    if choice == "1":
        users = user_service.find_by_name(query)
    elif choice == "2":
        users = user_service.find_by_email(query)
    else:
        click.echo("Invalid choice.")
        return

    if isinstance(users, list) and users:
        for user in users:
            click.echo(f"ID: {user.id}, Name: {user.name}, Email: {user.email}")
    else:
        click.echo(f"No users found with that attribute.")

# ============= Book Management Menu =============

def manage_books():
    """Displays the book management menu."""
    while True:
        click.echo("\n===== Book Management =====")
        click.echo("1. Add a new book")
        click.echo("2. Delete a book")
        click.echo("3. List all books")
        click.echo("4. Search for a book")
        click.echo("5. Back to Main Menu")
        
        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_book()
        elif choice == "2":
            delete_book()
        elif choice == "3":
            list_books()
        elif choice == "4":
            search_books()
        elif choice == "5":
            break
        else:
            click.echo("Invalid option. Please choose again.")

def add_book():
    """Prompt the user to add a new book."""
    title = input("Enter book title: ").strip()
    author = input("Enter book author: ").strip()
    available = input("Enter number of available copies: ").strip()
    genres = input("Enter genres (optional): ").strip()

    result = book_service.add_book(title, author, int(available), genres)
    click.echo(result)

def delete_book():
    """Prompt the user to delete a book by ID."""
    book_id = input("Enter book ID to delete: ").strip()
    
    result = book_service.delete_book(int(book_id))
    click.echo(result)

def list_books():
    """List all available books."""
    books = book_service.list_books()
    if isinstance(books, list):
        click.echo("\nBooks:")
        for book in books:
            click.echo(book)
    else:
        click.echo(books)

def search_books():
    """Search for books by title or author."""
    title = input("Enter book title to search (leave blank to skip): ").strip()
    author = input("Enter book author to search (leave blank to skip): ").strip()

    books = book_service.search_books(title=title, author=author)
    if books:
        click.echo("\nSearch Results:")
        for book in books:
            click.echo(f"ID: {book.id}, Title: {book.title}, Author: {book.author}, Available: {book.available}")
    else:
        click.echo("No books found.")

# ============= Rental Management Menu =============

def manage_rentals():
    """Displays the rental management menu."""
    while True:
        click.echo("\n===== Rental Management =====")
        click.echo("1. Rent a book by ID")
        click.echo("2. Rent a book by name and title (for seed data or simulated overdue returns)")
        click.echo("3. Return a book")
        click.echo("4. List active rentals")
        click.echo("5. Back to Main Menu")
        
        choice = input("Choose an option: ").strip()

        if choice == "1":
            rent_book_by_id()
        elif choice == "2":
            rent_book_by_name_and_title()
        elif choice == "3":
            return_book()
        elif choice == "4":
            list_rentals()
        elif choice == "5":
            break
        else:
            click.echo("Invalid option. Please choose again.")

def rent_book_by_id():
    """Prompt the user to rent a book by user ID and book ID."""
    user_id = input("Enter user ID: ").strip()
    book_id = input("Enter book ID: ").strip()

    result = rental_service.rent_book(int(user_id), int(book_id))
    click.echo(result)

def rent_book_by_name_and_title():
    """Rent a book using the user name and book title. Can simulate overdue returns."""
    user_name = input("Enter user name: ").strip()
    book_title = input("Enter book title: ").strip()
    days_rented_ago = input("Enter days rented ago (default 0): ").strip() or 0
    due_days_ago = input("Enter overdue days (default 0, enter to skip): ").strip() or 0

    result = rental_service.rent_book_by_name(user_name, book_title, int(days_rented_ago), int(due_days_ago))
    click.echo(result)

def return_book():
    """Prompt the user to return a rented book."""
    rental_id = input("Enter rental ID to return: ").strip()

    result = rental_service.return_book(int(rental_id))
    click.echo(result)

def list_rentals():
    """List all active rentals and returned rentals sorted by return date."""
    rentals = rental_service.list_rentals()
    if isinstance(rentals, list):
        click.echo("\n".join(rentals))
    else:
        click.echo(rentals)

# ============= Main Execution =============

if __name__ == '__main__':
    main_menu()
