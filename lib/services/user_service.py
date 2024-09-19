from lib.models import User
from sqlalchemy.exc import IntegrityError
from lib.database import get_session

class UserService:
    def add_user(self, name, email):
        """Add a new user to the system"""
        session = get_session()
        try:
            if not name or not email:
                raise ValueError("Both name and email are required.")
            user = User(name=name, email=email)
            session.add(user)
            session.commit()
            return f"User '{name}' added successfully with ID: {user.id}"
        except IntegrityError:
            session.rollback()
            return "Error: Email already exists."
        finally:
            session.close()

    def delete_user(self, user_id):
        """Delete a user by their ID"""
        session = get_session()
        try:
            user = session.get(User, user_id)
            if not user:
                return f"Error: User with ID {user_id} does not exist."
            session.delete(user)
            session.commit()
            return f"User ID {user_id} successfully deleted."
        finally:
            session.close()

    def list_users(self):
        """List all users"""
        session = get_session()
        users = session.query(User).all()
        session.close()
        if users:
            return [f"User ID: {user.id}, Name: {user.name}, Email: {user.email}" for user in users]
        return "No users found."
