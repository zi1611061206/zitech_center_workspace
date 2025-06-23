"""
Unit Tests for MCP Server Management Module

This file contains unit tests for the MCP Server Management module, ensuring the functionality
of the MCPServerMarketplace and MCPServerDriver classes.
"""

import unittest
from unittest.mock import MagicMock
from zi_coder_agent.mcp_server_management import MCPServerMarketplace, MCPServerDriver

class MockMCPServerDriver(MCPServerDriver):
    """Mock implementation of MCPServerDriver for testing purposes."""
    
    def connect(self) -> bool:
        return True
    
    def disconnect(self) -> bool:
        return True
    
    def get_tools(self) -> list:
        return ["tool1", "tool2"]
    
    def get_resources(self) -> list:
        return ["resource1", "resource2"]
    
    def use_tool(self, tool_name: str, arguments: dict) -> dict:
        return {"result": f"Used {tool_name} with {arguments}"}
    
    def access_resource(self, uri: str) -> dict:
        return {"data": f"Accessed {uri}"}

class TestMCPServerMarketplace(unittest.TestCase):
    """Test suite for MCPServerMarketplace class."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.marketplace = MCPServerMarketplace()
    
    def test_register_driver(self):
        """Test registering a new MCP server driver."""
        self.marketplace.register_driver("mock", MockMCPServerDriver)
        self.assertIn("mock", self.marketplace._drivers)
        self.assertIsInstance(self.marketplace._drivers["mock"], MockMCPServerDriver)
    
    def test_set_active_driver(self):
        """Test setting an active driver."""
        self.marketplace.register_driver("mock", MockMCPServerDriver)
        result = self.marketplace.set_active_driver("mock")
        self.assertTrue(result)
        self.assertIsInstance(self.marketplace._active_driver, MockMCPServerDriver)
    
    def test_set_active_driver_not_found(self):
        """Test setting an active driver that doesn't exist."""
        result = self.marketplace.set_active_driver("nonexistent")
        self.assertFalse(result)
        self.assertIsNone(self.marketplace._active_driver)
    
    def test_connect_with_active_driver(self):
        """Test connecting with an active driver."""
        self.marketplace.register_driver("mock", MockMCPServerDriver)
        self.marketplace.set_active_driver("mock")
        result = self.marketplace.connect()
        self.assertTrue(result)
    
    def test_connect_without_active_driver(self):
        """Test connecting without an active driver."""
        result = self.marketplace.connect()
        self.assertFalse(result)
    
    def test_get_tools_with_active_driver(self):
        """Test getting tools with an active driver."""
        self.marketplace.register_driver("mock", MockMCPServerDriver)
        self.marketplace.set_active_driver("mock")
        tools = self.marketplace.get_tools()
        self.assertEqual(tools, ["tool1", "tool2"])
    
    def test_get_tools_without_active_driver(self):
        """Test getting tools without an active driver."""
        tools = self.marketplace.get_tools()
        self.assertIsNone(tools)
    
    def test_disconnect_with_active_driver(self):
        """Test disconnecting with an active driver."""
        self.marketplace.register_driver("mock", MockMCPServerDriver)
        self.marketplace.set_active_driver("mock")
        result = self.marketplace.disconnect()
        self.assertTrue(result)
    
    def test_disconnect_without_active_driver(self):
        """Test disconnecting without an active driver."""
        result = self.marketplace.disconnect()
        self.assertFalse(result)
    
    def test_get_resources_with_active_driver(self):
        """Test getting resources with an active driver."""
        self.marketplace.register_driver("mock", MockMCPServerDriver)
        self.marketplace.set_active_driver("mock")
        resources = self.marketplace.get_resources()
        self.assertEqual(resources, ["resource1", "resource2"])
    
    def test_get_resources_without_active_driver(self):
        """Test getting resources without an active driver."""
        resources = self.marketplace.get_resources()
        self.assertIsNone(resources)
    
    def test_use_tool_with_active_driver(self):
        """Test using a tool with an active driver."""
        self.marketplace.register_driver("mock", MockMCPServerDriver)
        self.marketplace.set_active_driver("mock")
        result = self.marketplace.use_tool("tool1", {"arg": "value"})
        self.assertEqual(result, {"result": "Used tool1 with {'arg': 'value'}"})
    
    def test_use_tool_without_active_driver(self):
        """Test using a tool without an active driver."""
        result = self.marketplace.use_tool("tool1", {"arg": "value"})
        self.assertIsNone(result)
    
    def test_access_resource_with_active_driver(self):
        """Test accessing a resource with an active driver."""
        self.marketplace.register_driver("mock", MockMCPServerDriver)
        self.marketplace.set_active_driver("mock")
        result = self.marketplace.access_resource("uri/test")
        self.assertEqual(result, {"data": "Accessed uri/test"})
    
    def test_access_resource_without_active_driver(self):
        """Test accessing a resource without an active driver."""
        result = self.marketplace.access_resource("uri/test")
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
