"""
MCP Server Management Module

This module provides a pluggable driver system for managing connections to multiple MCP servers.
It is designed with extensibility in mind, following SOLID principles and MCP specifications.
"""

from abc import ABC, abstractmethod
from typing import Dict, Type, Optional

class MCPServerDriver(ABC):
    """Abstract base class for MCP server drivers."""
    
    @abstractmethod
    def connect(self) -> bool:
        """Establish connection to the MCP server."""
        pass
    
    @abstractmethod
    def disconnect(self) -> bool:
        """Disconnect from the MCP server."""
        pass
    
    @abstractmethod
    def get_tools(self) -> list:
        """Retrieve available tools from the MCP server."""
        pass
    
    @abstractmethod
    def get_resources(self) -> list:
        """Retrieve available resources from the MCP server."""
        pass
    
    @abstractmethod
    def use_tool(self, tool_name: str, arguments: dict) -> dict:
        """Use a specific tool from the MCP server with provided arguments."""
        pass
    
    @abstractmethod
    def access_resource(self, uri: str) -> dict:
        """Access a specific resource from the MCP server."""
        pass

class MCPServerMarketplace:
    """Manages multiple MCP server drivers for different MCP servers."""
    
    def __init__(self):
        self._drivers: Dict[str, MCPServerDriver] = {}
        self._active_driver: Optional[MCPServerDriver] = None
    
    def register_driver(self, name: str, driver: Type[MCPServerDriver]) -> None:
        """
        Register a new MCP server driver.
        
        Args:
            name: Unique identifier for the driver.
            driver: The driver class to register.
        """
        self._drivers[name] = driver()
    
    def set_active_driver(self, name: str) -> bool:
        """
        Set the active driver for MCP server interactions.
        
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
        Connect to the active MCP server driver.
        
        Returns:
            bool: True if connection was successful, False otherwise.
        """
        if self._active_driver:
            return self._active_driver.connect()
        return False
    
    def disconnect(self) -> bool:
        """
        Disconnect from the active MCP server driver.
        
        Returns:
            bool: True if disconnection was successful, False otherwise.
        """
        if self._active_driver:
            return self._active_driver.disconnect()
        return False
    
    def get_tools(self) -> Optional[list]:
        """
        Retrieve available tools from the active MCP server driver.
        
        Returns:
            Optional[list]: List of tools, or None if no active driver.
        """
        if self._active_driver:
            return self._active_driver.get_tools()
        return None
    
    def get_resources(self) -> Optional[list]:
        """
        Retrieve available resources from the active MCP server driver.
        
        Returns:
            Optional[list]: List of resources, or None if no active driver.
        """
        if self._active_driver:
            return self._active_driver.get_resources()
        return None
    
    def use_tool(self, tool_name: str, arguments: dict) -> Optional[dict]:
        """
        Use a specific tool from the active MCP server driver.
        
        Args:
            tool_name: Name of the tool to use.
            arguments: Arguments to pass to the tool.
            
        Returns:
            Optional[dict]: Result from the tool, or None if no active driver.
        """
        if self._active_driver:
            return self._active_driver.use_tool(tool_name, arguments)
        return None
    
    def access_resource(self, uri: str) -> Optional[dict]:
        """
        Access a specific resource from the active MCP server driver.
        
        Args:
            uri: URI of the resource to access.
            
        Returns:
            Optional[dict]: Resource data, or None if no active driver.
        """
        if self._active_driver:
            return self._active_driver.access_resource(uri)
        return None
