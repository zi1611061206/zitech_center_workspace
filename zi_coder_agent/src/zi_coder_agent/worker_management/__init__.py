"""
Worker Management Module

This module provides a pluggable driver system for managing connections to worker queue systems like Celery, RabbitMQ, etc.
It is designed with extensibility in mind, following SOLID principles.
"""

from abc import ABC, abstractmethod
from typing import Dict, Type, Optional, Any

class WorkerDriver(ABC):
    """Abstract base class for worker queue drivers."""
    
    @abstractmethod
    def connect(self) -> bool:
        """Establish connection to the worker queue system."""
        pass
    
    @abstractmethod
    def disconnect(self) -> bool:
        """Disconnect from the worker queue system."""
        pass
    
    @abstractmethod
    def enqueue_task(self, task_name: str, args: tuple = (), kwargs: dict = {}) -> str:
        """
        Enqueue a task to be processed by workers.
        
        Args:
            task_name: The name of the task to enqueue.
            args: Positional arguments for the task.
            kwargs: Keyword arguments for the task.
            
        Returns:
            str: Task ID or identifier for tracking.
        """
        pass
    
    @abstractmethod
    def get_task_status(self, task_id: str) -> Optional[dict]:
        """
        Retrieve the status of a specific task.
        
        Args:
            task_id: The ID of the task to check.
            
        Returns:
            Optional[dict]: Task status information, or None if not found.
        """
        pass
    
    @abstractmethod
    def get_task_result(self, task_id: str) -> Optional[Any]:
        """
        Retrieve the result of a completed task.
        
        Args:
            task_id: The ID of the task to retrieve result for.
            
        Returns:
            Optional[Any]: Task result if completed, None otherwise.
        """
        pass

class QueueToolMarketplace:
    """Manages multiple worker queue drivers for different queue systems."""
    
    def __init__(self):
        self._drivers: Dict[str, WorkerDriver] = {}
        self._active_driver: Optional[WorkerDriver] = None
    
    def register_driver(self, name: str, driver: Type[WorkerDriver]) -> None:
        """
        Register a new worker queue driver.
        
        Args:
            name: Unique identifier for the driver.
            driver: The driver class to register.
        """
        self._drivers[name] = driver()
    
    def set_active_driver(self, name: str) -> bool:
        """
        Set the active driver for worker queue interactions.
        
        Args:
            name: Name of the driver to activate.
            
        Returns:
            bool: True if driver was set successfully, False otherwise.
        """
        if name in self._drivers:
            self._active_driver = self._drivers[name]
            return True
        return False
    
    def connect(self) -> bool:
        """
        Connect to the active worker queue driver.
        
        Returns:
            bool: True if connection was successful, False otherwise.
        """
        if self._active_driver:
            return self._active_driver.connect()
        return False
    
    def disconnect(self) -> bool:
        """
        Disconnect from the active worker queue driver.
        
        Returns:
            bool: True if disconnection was successful, False otherwise.
        """
        if self._active_driver:
            return self._active_driver.disconnect()
        return False
    
    def enqueue_task(self, task_name: str, args: tuple = (), kwargs: dict = {}) -> Optional[str]:
        """
        Enqueue a task using the active worker queue driver.
        
        Args:
            task_name: The name of the task to enqueue.
            args: Positional arguments for the task.
            kwargs: Keyword arguments for the task.
            
        Returns:
            Optional[str]: Task ID if successful, None otherwise.
        """
        if self._active_driver:
            return self._active_driver.enqueue_task(task_name, args, kwargs)
        return None
    
    def get_task_status(self, task_id: str) -> Optional[dict]:
        """
        Retrieve the status of a specific task using the active driver.
        
        Args:
            task_id: The ID of the task to check.
            
        Returns:
            Optional[dict]: Task status information, or None if not found or no active driver.
        """
        if self._active_driver:
            return self._active_driver.get_task_status(task_id)
        return None
    
    def get_task_result(self, task_id: str) -> Optional[Any]:
        """
        Retrieve the result of a completed task using the active driver.
        
        Args:
            task_id: The ID of the task to retrieve result for.
            
        Returns:
            Optional[Any]: Task result if completed, None otherwise.
        """
        if self._active_driver:
            return self._active_driver.get_task_result(task_id)
        return None
