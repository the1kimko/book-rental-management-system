from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Table, Float
from sqlalchemy.orm import relationship, sessionmaker, declarative_base
from datetime import datetime, timedelta, timezone

Base = declarative_base()

DATABASE_URL = "sqlite:///book_rental.db"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)


# Association table with a unique 'id' column
class UserBook(Base):
    __tablename__ = 'user_books'
    id = Column(Integer, primary_key=True)  # Unique ID for each row
    user_id = Column(Integer, ForeignKey('users.id'))
    book_id = Column(Integer, ForeignKey('books.id'))

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)

    # Many-to-many relationship through association table
    books = relationship("Book", secondary="user_books", back_populates="users")

    # Relationship to track rental records
    rentals = relationship("Rental", back_populates="user")

    def __repr__(self):
        return f"<User(name={self.name}, email={self.email})>"

class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    available = Column(Integer, default=1)

    # Many-to-many relationship through association table
    users = relationship("User", secondary="user_books", back_populates="books")

    # Relationship to track rental records
    rentals = relationship("Rental", back_populates="book")

    def __repr__(self):
        return f"<Book(title={self.title}, author={self.author})>"

class Rental(Base):
    __tablename__ = 'rentals'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    book_id = Column(Integer, ForeignKey('books.id'), nullable=False)
    rent_date = Column(DateTime, default=datetime.utcnow)
    return_date = Column(DateTime, nullable=True)
    due_date = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc) + timedelta(days=14))
    penalty = Column(Float, default=0.0)

    user = relationship("User", back_populates="rentals")
    book = relationship("Book", back_populates="rentals")

    def calculate_penalty(self):
        if self.return_date and self.return_date > self.due_date:
            days_late = (self.return_date - self.due_date).days
            self.penalty = days_late * 50  # KSh 50 per day late
        else:
            self.penalty = 0.0
        session.commit()

Base.metadata.create_all(engine)