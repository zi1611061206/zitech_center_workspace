"""
Unit Tests for Cache Management Module

This file contains unit tests for the Cache Management module, ensuring the functionality
of the CacheToolMarketplace and CacheDriver classes.
"""

import unittest
from unittest.mock import MagicMock
from zi_coder_agent.cache_management import CacheToolMarketplace, CacheDriver

class MockCacheDriver(CacheDriver):
    """Mock implementation of CacheDriver for testing purposes."""
    
    def connect(self) -> bool:
        return True
    
    def disconnect(self) -> bool:
        return True
    
    def set(self, key: str, value: any, ttl: int = None) -> bool:
        return True
    
    def get(self, key: str) -> any:
        return f"Value for {key}"
    
    def delete(self, key: str) -> bool:
        return True
    
    def clear(self) -> bool:
        return True

class TestCacheToolMarketplace(unittest.TestCase):
    """Test suite for CacheToolMarketplace class."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.marketplace = CacheToolMarketplace()
    
    def test_register_driver(self):
        """Test registering a new cache driver."""
        self.marketplace.register_driver("mock", MockCacheDriver)
        self.assertIn("mock", self.marketplace._drivers)
        self.assertIsInstance(self.marketplace._drivers["mock"], MockCacheDriver)
    
    def test_set_active_driver(self):
        """Test setting an active driver."""
        self.marketplace.register_driver("mock", MockCacheDriver)
        result = self.marketplace.set_active_driver("mock")
        self.assertTrue(result)
        self.assertIsInstance(self.marketplace._active_driver, MockCacheDriver)
    
    def test_set_active_driver_not_found(self):
        """Test setting an active driver that doesn't exist."""
        result = self.marketplace.set_active_driver("nonexistent")
        self.assertFalse(result)
        self.assertIsNone(self.marketplace._active_driver)
    
    def test_connect_with_active_driver(self):
        """Test connecting with an active driver."""
        self.marketplace.register_driver("mock", MockCacheDriver)
        self.marketplace.set_active_driver("mock")
        result = self.marketplace.connect()
        self.assertTrue(result)
    
    def test_connect_without_active_driver(self):
        """Test connecting without an active driver."""
        result = self.marketplace.connect()
        self.assertFalse(result)
    
    def test_set_with_active_driver(self):
        """Test setting a cache value with an active driver."""
        self.marketplace.register_driver("mock", MockCacheDriver)
        self.marketplace.set_active_driver("mock")
        result = self.marketplace.set("key", "value", 3600)
        self.assertTrue(result)
    
    def test_set_without_active_driver(self):
        """Test setting a cache value without an active driver."""
        result = self.marketplace.set("key", "value", 3600)
        self.assertFalse(result)
    
    def test_get_with_active_driver(self):
        """Test getting a cache value with an active driver."""
        self.marketplace.register_driver("mock", MockCacheDriver)
        self.marketplace.set_active_driver("mock")
        value = self.marketplace.get("key")
        self.assertEqual(value, "Value for key")
    
    def test_disconnect_with_active_driver(self):
        """Test disconnecting with an active driver."""
        self.marketplace.register_driver("mock", MockCacheDriver)
        self.marketplace.set_active_driver("mock")
        result = self.marketplace.disconnect()
        self.assertTrue(result)
    
    def test_disconnect_without_active_driver(self):
        """Test disconnecting without an active driver."""
        result = self.marketplace.disconnect()
        self.assertFalse(result)
    
    def test_delete_with_active_driver(self):
        """Test deleting a cache value with an active driver."""
        self.marketplace.register_driver("mock", MockCacheDriver)
        self.marketplace.set_active_driver("mock")
        result = self.marketplace.delete("key")
        self.assertTrue(result)
    
    def test_delete_without_active_driver(self):
        """Test deleting a cache value without an active driver."""
        result = self.marketplace.delete("key")
        self.assertFalse(result)
    
    def test_clear_with_active_driver(self):
        """Test clearing all cache values with an active driver."""
        self.marketplace.register_driver("mock", MockCacheDriver)
        self.marketplace.set_active_driver("mock")
        result = self.marketplace.clear()
        self.assertTrue(result)
    
    def test_clear_without_active_driver(self):
        """Test clearing all cache values without an active driver."""
        result = self.marketplace.clear()
        self.assertFalse(result)
    
    def test_get_without_active_driver(self):
        """Test getting a cache value without an active driver."""
        value = self.marketplace.get("key")
        self.assertIsNone(value)

if __name__ == '__main__':
    unittest.main()
