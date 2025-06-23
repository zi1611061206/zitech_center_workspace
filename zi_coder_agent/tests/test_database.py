"""
Unit Tests for Database Module

This file contains unit tests for the Database module, ensuring the functionality
of the DatabaseManager class.
"""

import unittest
from unittest.mock import MagicMock, patch
from zi_coder_agent.database import DatabaseManager, engine, SessionLocal

class TestDatabaseManager(unittest.TestCase):
    """Test suite for DatabaseManager class."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.db_manager = DatabaseManager()
    
    @patch('sqlalchemy.engine.base.Engine.connect')
    def test_connect_success(self, mock_connect):
        """Test successful database connection."""
        mock_connect.return_value = MagicMock()
        result = self.db_manager.connect()
        self.assertTrue(result)
        mock_connect.assert_called_once()
    
    @patch('sqlalchemy.engine.base.Engine.connect')
    def test_connect_failure(self, mock_connect):
        """Test failed database connection."""
        mock_connect.side_effect = Exception("Connection failed")
        result = self.db_manager.connect()
        self.assertFalse(result)
        mock_connect.assert_called_once()
    
    @patch('sqlalchemy.engine.base.Engine.dispose')
    def test_disconnect_success(self, mock_dispose):
        """Test successful database disconnection."""
        mock_session = MagicMock()
        self.db_manager._current_session = mock_session
        result = self.db_manager.disconnect()
        self.assertTrue(result)
        mock_session.close.assert_called_once()
        mock_dispose.assert_called_once()
        self.assertIsNone(self.db_manager._current_session)
    
    @patch('sqlalchemy.engine.base.Engine.dispose')
    def test_disconnect_failure(self, mock_dispose):
        """Test failed database disconnection."""
        mock_dispose.side_effect = Exception("Disconnection failed")
        mock_session = MagicMock()
        self.db_manager._current_session = mock_session
        result = self.db_manager.disconnect()
        self.assertFalse(result)
        mock_session.close.assert_called_once()
        mock_dispose.assert_called_once()
    
    def test_get_session(self):
        """Test getting a database session."""
        session = self.db_manager.get_session()
        self.assertIsNotNone(session)
        # Avoid isinstance check due to Python 3.13 compatibility issues
        self.assertEqual(self.db_manager._current_session, session)
    
    @patch('zi_coder_agent.database.Base.metadata.create_all')
    def test_create_all(self, mock_create_all):
        """Test creating all database tables."""
        self.db_manager.create_all()
        mock_create_all.assert_called_once_with(bind=engine)
    
    @patch('zi_coder_agent.database.Base.metadata.drop_all')
    def test_drop_all(self, mock_drop_all):
        """Test dropping all database tables."""
        self.db_manager.drop_all()
        mock_drop_all.assert_called_once_with(bind=engine)

if __name__ == '__main__':
    unittest.main()
