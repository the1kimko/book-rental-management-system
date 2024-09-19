# Book Rental Management System

## Overview
The Book Rental Management System is a command-line interface (CLI) application that allows users to manage book rentals. It tracks books, users, rentals, and handles the business logic of renting and returning books. The project is modular, following object-oriented programming (OOP) principles, and uses SQLAlchemy as an ORM to interact with the database.

The system features:

- User management (adding, deleting, listing users).
- Book management (adding, deleting, listing, and searching books).
- Rental management (renting and returning books).
- Validation to prevent users from renting the same book multiple times unless returned.
- Sorting functionality for rentals based on return dates and genres.

## Technologies Used
1. Python: Main programming language for this project.
2. Click: A package used to build the CLI.
3. SQLAlchemy: An ORM to interact with SQLite.
4. Alembic: A database migration tool used to track and apply schema changes.
5. SQLite: Database used for local development.

## Project Structure
```bash
.
├── alembic.ini                # Alembic configuration
├── book_rental.db             # SQLite database file
├── lib                        # Main project directory
│   ├── __init__.py
│   ├── cli.py                 # Main CLI interface
│   ├── models.py              # SQLAlchemy models
│   ├── services               # Service classes for User, Book, and Rental management
│   │   ├── __init__.py
│   │   ├── book_service.py
│   │   ├── rental_service.py
│   │   └── user_service.py
├── migrations                 # Directory for alembic migrations
│   ├── env.py                 # Alembic environment
│   └── versions               # Migration versions
├── Pipfile                    # Pipenv file to manage dependencies
├── seed.py                    # Script to seed the database
├── README.md                  # Project documentation
```

## Set-Up Instructions

### Requirements
Ensure you have the following installed:

- Python (>= 3.9)
- Pipenv (for managing dependencies)
- SQLite (comes pre-installed with Python)

### Steps to Set-Up the Project Locally

a. Clone the repository:
```bash
git clone https://github.com/the1kimko/book-rental-management-system.git
cd book-rental-management-system
```

b. Install dependencies:
```bash
pip install pipenv
pipenv install
```

c. Activate the virtual environment:
```bash
pipenv shell
```

d. Set up the SQLite database: The database file (`book_rental.db`) is generated automatically when you run migrations.

e. Run Alembic migrations to create the database schema:
```bash
alembic upgrade head
```
This will create all necessary tables (books, users, rentals, and user_books for many-to-many relationships).

f. Seed the database with initial data (optional): You can populate the database with users, books, and rentals using the seed.py script:
```bash
python seed.py
```

## Database Structure and Relationships
The database consists of the following tables:

1. Users: Stores information about users such as `name` and `email`.
2. Books: Stores details about books, including `title`, `author`, `available` copies, and `genres`.
3. Rentals: Tracks which user rented which book, when they rented it, the due date, return date, and any penalties incurred.
4. User_Books: An association table that represents a many-to-many relationship between users and books, facilitated by the `rentals` table.

### Table Relationships:
- One-to-Many: A user can have many rentals, but a rental is tied to only one user.
- One-to-Many: A book can have many rentals, but a rental is tied to only one book.
- Many-to-Many: Users and books have a many-to-many relationship through the rentals table. A user can rent multiple books, and a book can be rented by multiple users over time.

## Alembic Migrations
### Alembic Overview:
Alembic is used for database schema management. Migrations are stored in the `migrations/versions` folder.

Alembic Configuration:
The `alembic.ini` file provides the basic configurations for Alembic.

The `migrations/env.py` file is responsible for setting up the migration environment, loading the SQLAlchemy models, and running migrations.

### Creating and Running Migrations:
1. To create a new migration after making changes to the models:
```bash
alembic revision --autogenerate -m "Migration message"
```

2. To apply migrations to the database:
```bash
alembic upgrade head
```

3. To revert the last migration:
```bash
alembic downgrade -1
```

## CLI Commands and Usage
The CLI interface allows you to interact with the system via commands. Here's a breakdown of available commands:

### User Commands:

- Add a User:
```bash
python -m lib.cli add-user "John Doe" "john@example.com"
```

- List All Users:
```bash
python -m lib.cli list-users
```

- Delete a User:
```bash
python -m lib.cli delete-user 1  # Deletes user with ID 1
```

### Book Commands:

- Add a Book:
```bash
python -m lib.cli add-book "1984" "George Orwell" --available 5 --genres "Dystopian"
```

- List All Books:
```bash
python -m lib.cli list-books
```

- Search Books by Title/Author:
```bash
python -m lib.cli search-books --title "1984"
python -m lib.cli search-books --author "George Orwell"
```

- Delete a Book:
```bash
python -m lib.cli delete-book 1  # Deletes book with ID 1
```

### Rental Commands:

- Rent a Book:
```bash
python -m lib.cli rent-book 1 1  # User with ID 1 rents book with ID 1
```

- Return a Book:
```bash
python -m lib.cli return-book 1  # Return rental with ID 1
```

- List All Rentals:
```bash
python -m lib.cli list-rentals
```

### Other Commands:
- Calculate Penalty for Late Returns:
```bash
python -m lib.cli calculate-penalty 1  # Calculates penalty for rental with ID 1
```

## Testing and Debugging
For testing purposes, a `debug.py` file is provided to seed data, test rental functionality, and validate the system behavior. You can run it to automatically test the flow of adding users, books, and rentals:

```bash
python debug.py
```

## Contributing
Feel free to fork the project and submit pull requests. Make sure to run all tests before submitting a pull request. Any improvements to CLI functionalities or the overall structure are welcome!

## License
This project is licensed under the MIT License.


