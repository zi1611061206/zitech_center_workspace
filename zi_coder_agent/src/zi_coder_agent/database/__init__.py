"""
Database Layer Module

This module provides the database access layer using SQLAlchemy as the ORM and Alembic for version-controlled migrations.
It is designed to manage database connections and operations for the application.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import Optional

# Database configuration
import os
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///test.db")
if "pytest" in os.environ.get("PYTEST_CURRENT_TEST", ""):
    DATABASE_URL = "sqlite:///test.db"

# SQLAlchemy setup
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    """
    Get a database session for use in dependency injection.
    
    Yields:
        Session: A SQLAlchemy session for database operations.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class DatabaseManager:
    """Manages database connections and operations."""
    
    def __init__(self):
        self._engine = engine
        self._session_factory = SessionLocal
        self._current_session: Optional[SessionLocal] = None
    
    def connect(self) -> bool:
        """
        Establish a connection to the database.
        
        Returns:
            bool: True if connection was successful, False otherwise.
        """
        try:
            self._engine.connect()
            return True
        except Exception as e:
            print(f"Database connection failed: {e}")
            return False
    
    def disconnect(self) -> bool:
        """
        Disconnect from the database.
        
        Returns:
            bool: True if disconnection was successful, False otherwise.
        """
        try:
            if self._current_session:
                self._current_session.close()
                self._current_session = None
            self._engine.dispose()
            return True
        except Exception as e:
            print(f"Database disconnection failed: {e}")
            return False
    
    def get_session(self) -> SessionLocal:
        """
        Get or create a database session.
        
        Returns:
            SessionLocal: A SQLAlchemy session for database operations.
        """
        if not self._current_session:
            self._current_session = self._session_factory()
        return self._current_session
    
    def create_all(self) -> None:
        """
        Create all database tables defined in the models.
        """
        Base.metadata.create_all(bind=self._engine)
    
    def drop_all(self) -> None:
        """
        Drop all database tables.
        """
        Base.metadata.drop_all(bind=self._engine)
