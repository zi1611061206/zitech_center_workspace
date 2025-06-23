"""
Caching Management Module

This module provides a pluggable driver system for connecting to caching databases such as Redis, Memcached, etc.
It is designed with extensibility in mind, following SOLID principles.
"""

from abc import ABC, abstractmethod
from typing import Dict, Type, Optional, Any

class CacheDriver(ABC):
    """Abstract base class for cache drivers."""
    
    @abstractmethod
    def connect(self) -> bool:
        """Establish connection to the cache database."""
        pass
    
    @abstractmethod
    def disconnect(self) -> bool:
        """Disconnect from the cache database."""
        pass
    
    @abstractmethod
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """
        Set a value in the cache.
        
        Args:
            key: The key for the cache entry.
            value: The value to store.
            ttl: Time to live in seconds, if applicable.
            
        Returns:
            bool: True if set operation was successful, False otherwise.
        """
        pass
    
    @abstractmethod
    def get(self, key: str) -> Optional[Any]:
        """
        Retrieve a value from the cache.
        
        Args:
            key: The key of the cache entry to retrieve.
            
        Returns:
            Optional[Any]: The value if found, None otherwise.
        """
        pass
    
    @abstractmethod
    def delete(self, key: str) -> bool:
        """
        Delete a value from the cache.
        
        Args:
            key: The key of the cache entry to delete.
            
        Returns:
            bool: True if deletion was successful, False otherwise.
        """
        pass
    
    @abstractmethod
    def clear(self) -> bool:
        """
        Clear all cache entries.
        
        Returns:
            bool: True if clear operation was successful, False otherwise.
        """
        pass

class CacheToolMarketplace:
    """Manages multiple cache drivers for different caching systems."""
    
    def __init__(self):
        self._drivers: Dict[str, CacheDriver] = {}
        self._active_driver: Optional[CacheDriver] = None
    
    def register_driver(self, name: str, driver: Type[CacheDriver]) -> None:
        """
        Register a new cache driver.
        
        Args:
            name: Unique identifier for the driver.
            driver: The driver class to register.
        """
        self._drivers[name] = driver()
    
    def set_active_driver(self, name: str) -> bool:
        """
        Set the active driver for cache interactions.
        
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
        Connect to the active cache driver.
        
        Returns:
            bool: True if connection was successful, False otherwise.
        """
        if self._active_driver:
            return self._active_driver.connect()
        return False
    
    def disconnect(self) -> bool:
        """
        Disconnect from the active cache driver.
        
        Returns:
            bool: True if disconnection was successful, False otherwise.
        """
        if self._active_driver:
            return self._active_driver.disconnect()
        return False
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """
        Set a value in the active cache driver.
        
        Args:
            key: The key for the cache entry.
            value: The value to store.
            ttl: Time to live in seconds, if applicable.
            
        Returns:
            bool: True if set operation was successful, False otherwise.
        """
        if self._active_driver:
            return self._active_driver.set(key, value, ttl)
        return False
    
    def get(self, key: str) -> Optional[Any]:
        """
        Retrieve a value from the active cache driver.
        
        Args:
            key: The key of the cache entry to retrieve.
            
        Returns:
            Optional[Any]: The value if found, None otherwise.
        """
        if self._active_driver:
            return self._active_driver.get(key)
        return None
    
    def delete(self, key: str) -> bool:
        """
        Delete a value from the active cache driver.
        
        Args:
            key: The key of the cache entry to delete.
            
        Returns:
            bool: True if deletion was successful, False otherwise.
        """
        if self._active_driver:
            return self._active_driver.delete(key)
        return False
    
    def clear(self) -> bool:
        """
        Clear all cache entries in the active driver.
        
        Returns:
            bool: True if clear operation was successful, False otherwise.
        """
        if self._active_driver:
            return self._active_driver.clear()
        return False
