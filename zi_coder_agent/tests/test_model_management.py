"""
Unit Tests for Model Management Module

This file contains unit tests for the Model Management module, ensuring the functionality
of the ModelMarketplace and ModelDriver classes.
"""

import unittest
from unittest.mock import MagicMock
from zi_coder_agent.model_management import ModelMarketplace, ModelDriver

class MockModelDriver(ModelDriver):
    """Mock implementation of ModelDriver for testing purposes."""
    
    def connect(self) -> bool:
        return True
    
    def disconnect(self) -> bool:
        return True
    
    def query(self, input_data: str) -> str:
        return f"Response to {input_data}"

class TestModelMarketplace(unittest.TestCase):
    """Test suite for ModelMarketplace class."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.marketplace = ModelMarketplace()
    
    def test_register_driver(self):
        """Test registering a new model driver."""
        self.marketplace.register_driver("mock", MockModelDriver)
        self.assertIn("mock", self.marketplace._drivers)
        self.assertIsInstance(self.marketplace._drivers["mock"], MockModelDriver)
    
    def test_set_active_driver(self):
        """Test setting an active driver."""
        self.marketplace.register_driver("mock", MockModelDriver)
        result = self.marketplace.set_active_driver("mock")
        self.assertTrue(result)
        self.assertIsInstance(self.marketplace._active_driver, MockModelDriver)
    
    def test_set_active_driver_not_found(self):
        """Test setting an active driver that doesn't exist."""
        result = self.marketplace.set_active_driver("nonexistent")
        self.assertFalse(result)
        self.assertIsNone(self.marketplace._active_driver)
    
    def test_connect_with_active_driver(self):
        """Test connecting with an active driver."""
        self.marketplace.register_driver("mock", MockModelDriver)
        self.marketplace.set_active_driver("mock")
        result = self.marketplace.connect()
        self.assertTrue(result)
    
    def test_connect_without_active_driver(self):
        """Test connecting without an active driver."""
        result = self.marketplace.connect()
        self.assertFalse(result)
    
    def test_disconnect_with_active_driver(self):
        """Test disconnecting with an active driver."""
        self.marketplace.register_driver("mock", MockModelDriver)
        self.marketplace.set_active_driver("mock")
        result = self.marketplace.disconnect()
        self.assertTrue(result)
    
    def test_disconnect_without_active_driver(self):
        """Test disconnecting without an active driver."""
        result = self.marketplace.disconnect()
        self.assertFalse(result)
    
    def test_query_with_active_driver(self):
        """Test querying with an active driver."""
        self.marketplace.register_driver("mock", MockModelDriver)
        self.marketplace.set_active_driver("mock")
        response = self.marketplace.query("test input")
        self.assertEqual(response, "Response to test input")
    
    def test_query_without_active_driver(self):
        """Test querying without an active driver."""
        response = self.marketplace.query("test input")
        self.assertIsNone(response)

if __name__ == '__main__':
    unittest.main()
