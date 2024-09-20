
from lib.cli import cli

if __name__ == "__main__":
    # This launches the CLI in debug mode
    cli()

# =====================================================
# HOW TO USE THIS DEBUG SCRIPT
# =====================================================
# This script provides examples of how to run various CLI commands
# using the 'python debug.py' format. Below are some examples:
#
# 1. Adding a user:
#    Usage: python debug.py add_user <name> <email>
#    Example: 
#       python debug.py add_user "John Doe" "john@example.com"
#
# 2. Deleting a user:
#    Usage: python debug.py delete_user <user_id>
#    Example:
#       python debug.py delete_user 1
#
# 3. Listing all users:
#    Usage: python debug.py list_users
#    Example:
#       python debug.py list_users
#
# 4. Adding a book:
#    Usage: python debug.py add_book <title> <author> --available <number of copies>
#    Example:
#       python debug.py add_book "1984" "George Orwell" --available 5
#
# 5. Deleting a book:
#    Usage: python debug.py delete_book <book_id>
#    Example:
#       python debug.py delete_book 2
#
# 6. Listing all books:
#    Usage: python debug.py list_books
#    Example:
#       python debug.py list_books
#
# 7. Searching for books by title or author:
#    Usage: python debug.py search_books --title <title> --author <author>
#    Example:
#       python debug.py search_books --title "1984"
#       python debug.py search_books --author "George Orwell"
#
# 8. Renting a book:
#    Usage: python debug.py rent_book <user_id> <book_id>
#    Example:
#       python debug.py rent_book 1 3
#
# 9. Returning a book:
#    Usage: python debug.py return_book <rental_id>
#    Example:
#       python debug.py return_book 1
#
# 10. Listing all active rentals:
#     Usage: python debug.py list_rentals
#     Example:
#        python debug.py list_rentals
# =====================================================
#
# You can test these commands by adjusting the arguments (e.g., IDs or names) 
# based on your database content.
#
# For example:
#    - First, run 'python debug.py add_user "John Doe" "john@example.com"' to add a user.
#    - Then, run 'python debug.py list_users' to see the list of users.
#    - After that, try adding books, renting them, or even deleting users/books.
#
# Make sure the database is initialized and accessible before running these commands.

