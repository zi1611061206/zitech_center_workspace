"""
Model Management Module

This module provides a pluggable driver system for managing connections to various LLM models.
It is designed with extensibility in mind, following SOLID principles and MCP specifications.
"""

from abc import ABC, abstractmethod
from typing import Dict, Type, Optional

class ModelDriver(ABC):
    """Abstract base class for model drivers."""
    
    @abstractmethod
    def connect(self) -> bool:
        """Establish connection to the model."""
        pass
    
    @abstractmethod
    def disconnect(self) -> bool:
        """Disconnect from the model."""
        pass
    
    @abstractmethod
    def query(self, input_data: str) -> str:
        """Send a query to the model and return the response."""
        pass

class ModelMarketplace:
    """Manages multiple model drivers for different LLM models."""
    
    def __init__(self):
        self._drivers: Dict[str, ModelDriver] = {}
        self._active_driver: Optional[ModelDriver] = None
    
    def register_driver(self, name: str, driver: Type[ModelDriver]) -> None:
        """
        Register a new model driver.
        
        Args:
            name: Unique identifier for the driver.
            driver: The driver class to register.
        """
        self._drivers[name] = driver()
    
    def set_active_driver(self, name: str) -> bool:
        """
        Set the active driver for model interactions.
        
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
        Connect to the active model driver.
        
        Returns:
            bool: True if connection was successful, False otherwise.
        """
        if self._active_driver:
            return self._active_driver.connect()
        return False
    
    def disconnect(self) -> bool:
        """
        Disconnect from the active model driver.
        
        Returns:
            bool: True if disconnection was successful, False otherwise.
        """
        if self._active_driver:
            return self._active_driver.disconnect()
        return False
    
    def query(self, input_data: str) -> Optional[str]:
        """
        Send a query to the active model driver.
        
        Args:
            input_data: The input data to send to the model.
            
        Returns:
            Optional[str]: Response from the model, or None if no active driver.
        """
        if self._active_driver:
            return self._active_driver.query(input_data)
        return None
