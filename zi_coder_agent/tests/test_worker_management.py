"""
Unit Tests for Worker Management Module

This file contains unit tests for the Worker Management module, ensuring the functionality
of the QueueToolMarketplace and WorkerDriver classes.
"""

import unittest
from unittest.mock import MagicMock
from zi_coder_agent.worker_management import QueueToolMarketplace, WorkerDriver

class MockWorkerDriver(WorkerDriver):
    """Mock implementation of WorkerDriver for testing purposes."""
    
    def connect(self) -> bool:
        return True
    
    def disconnect(self) -> bool:
        return True
    
    def enqueue_task(self, task_name: str, args: tuple = (), kwargs: dict = {}) -> str:
        return "task_123"
    
    def get_task_status(self, task_id: str) -> dict:
        return {"status": "completed", "task_id": task_id}
    
    def get_task_result(self, task_id: str) -> any:
        return f"Result for {task_id}"

class TestQueueToolMarketplace(unittest.TestCase):
    """Test suite for QueueToolMarketplace class."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.marketplace = QueueToolMarketplace()
    
    def test_register_driver(self):
        """Test registering a new worker driver."""
        self.marketplace.register_driver("mock", MockWorkerDriver)
        self.assertIn("mock", self.marketplace._drivers)
        self.assertIsInstance(self.marketplace._drivers["mock"], MockWorkerDriver)
    
    def test_set_active_driver(self):
        """Test setting an active driver."""
        self.marketplace.register_driver("mock", MockWorkerDriver)
        result = self.marketplace.set_active_driver("mock")
        self.assertTrue(result)
        self.assertIsInstance(self.marketplace._active_driver, MockWorkerDriver)
    
    def test_set_active_driver_not_found(self):
        """Test setting an active driver that doesn't exist."""
        result = self.marketplace.set_active_driver("nonexistent")
        self.assertFalse(result)
        self.assertIsNone(self.marketplace._active_driver)
    
    def test_connect_with_active_driver(self):
        """Test connecting with an active driver."""
        self.marketplace.register_driver("mock", MockWorkerDriver)
        self.marketplace.set_active_driver("mock")
        result = self.marketplace.connect()
        self.assertTrue(result)
    
    def test_connect_without_active_driver(self):
        """Test connecting without an active driver."""
        result = self.marketplace.connect()
        self.assertFalse(result)
    
    def test_enqueue_task_with_active_driver(self):
        """Test enqueuing a task with an active driver."""
        self.marketplace.register_driver("mock", MockWorkerDriver)
        self.marketplace.set_active_driver("mock")
        task_id = self.marketplace.enqueue_task("test_task", args=(1, 2), kwargs={"key": "value"})
        self.assertEqual(task_id, "task_123")
    
    def test_enqueue_task_without_active_driver(self):
        """Test enqueuing a task without an active driver."""
        task_id = self.marketplace.enqueue_task("test_task", args=(1, 2), kwargs={"key": "value"})
        self.assertIsNone(task_id)
    
    def test_disconnect_with_active_driver(self):
        """Test disconnecting with an active driver."""
        self.marketplace.register_driver("mock", MockWorkerDriver)
        self.marketplace.set_active_driver("mock")
        result = self.marketplace.disconnect()
        self.assertTrue(result)
    
    def test_disconnect_without_active_driver(self):
        """Test disconnecting without an active driver."""
        result = self.marketplace.disconnect()
        self.assertFalse(result)
    
    def test_get_task_status_with_active_driver(self):
        """Test getting task status with an active driver."""
        self.marketplace.register_driver("mock", MockWorkerDriver)
        self.marketplace.set_active_driver("mock")
        status = self.marketplace.get_task_status("task_123")
        self.assertEqual(status, {"status": "completed", "task_id": "task_123"})
    
    def test_get_task_status_without_active_driver(self):
        """Test getting task status without an active driver."""
        status = self.marketplace.get_task_status("task_123")
        self.assertIsNone(status)
    
    def test_get_task_result_with_active_driver(self):
        """Test getting task result with an active driver."""
        self.marketplace.register_driver("mock", MockWorkerDriver)
        self.marketplace.set_active_driver("mock")
        result = self.marketplace.get_task_result("task_123")
        self.assertEqual(result, "Result for task_123")
    
    def test_get_task_result_without_active_driver(self):
        """Test getting task result without an active driver."""
        result = self.marketplace.get_task_result("task_123")
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
