"""
Unit Tests for API Server Module

This file contains unit tests for the API Server module, ensuring the functionality
of the Flask application and its endpoints.
"""

import unittest
from unittest.mock import MagicMock, patch
from flask import Flask
from zi_coder_agent.api_server import create_app

class TestAPIServer(unittest.TestCase):
    """Test suite for API Server endpoints."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True
    
    def test_register_model_driver(self):
        """Test registering a new model driver via API."""
        response = self.client.post('/api/models/register', json={
            'name': 'mock_model',
            'driver_path': 'path.to.mock.driver'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Model driver mock_model registered', response.data)
    
    def test_register_model_driver_missing_data(self):
        """Test registering a model driver with missing data."""
        response = self.client.post('/api/models/register', json={})
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Missing name or driver_path', response.data)
    
    def test_set_active_model_driver(self):
        """Test setting an active model driver via API."""
        # First register a driver
        self.client.post('/api/models/register', json={
            'name': 'mock_model',
            'driver_path': 'path.to.mock.driver'
        })
        # Then set it as active (mocking the actual setting for simplicity)
        with patch('zi_coder_agent.model_management.ModelMarketplace.set_active_driver') as mock_set:
            mock_set.return_value = True
            response = self.client.put('/api/models/active/mock_model')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Active model driver set to mock_model', response.data)
    
    def test_set_active_model_driver_not_found(self):
        """Test setting an active model driver that doesn't exist."""
        with patch('zi_coder_agent.model_management.ModelMarketplace.set_active_driver') as mock_set:
            mock_set.return_value = False
            response = self.client.put('/api/models/active/nonexistent')
            self.assertEqual(response.status_code, 404)
            self.assertIn(b'Driver nonexistent not found', response.data)
    
    def test_connect_model(self):
        """Test connecting to a model via API."""
        with patch('zi_coder_agent.model_management.ModelMarketplace.connect') as mock_connect:
            mock_connect.return_value = True
            response = self.client.post('/api/models/connect')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Connected to model', response.data)
    
    def test_query_model(self):
        """Test querying a model via API."""
        with patch('zi_coder_agent.model_management.ModelMarketplace.query') as mock_query:
            mock_query.return_value = "Mock response"
            response = self.client.post('/api/models/query', json={'input': 'test input'})
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Mock response', response.data)
    
    def test_query_model_missing_input(self):
        """Test querying a model with missing input."""
        response = self.client.post('/api/models/query', json={})
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Missing input data', response.data)
    
    def test_register_cache_driver(self):
        """Test registering a new cache driver via API."""
        response = self.client.post('/api/cache/register', json={
            'name': 'mock_cache',
            'driver_path': 'path.to.mock.cache'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Cache driver mock_cache registered', response.data)
    
    def test_set_cache_value(self):
        """Test setting a cache value via API."""
        with patch('zi_coder_agent.cache_management.CacheToolMarketplace.set') as mock_set:
            mock_set.return_value = True
            response = self.client.post('/api/cache/set', json={
                'key': 'test_key',
                'value': 'test_value',
                'ttl': 3600
            })
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Cache value set for key test_key', response.data)
    
    def test_set_active_cache_driver(self):
        """Test setting an active cache driver via API."""
        self.client.post('/api/cache/register', json={
            'name': 'mock_cache',
            'driver_path': 'path.to.mock.cache'
        })
        with patch('zi_coder_agent.cache_management.CacheToolMarketplace.set_active_driver') as mock_set:
            mock_set.return_value = True
            response = self.client.put('/api/cache/active/mock_cache')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Active cache driver set to mock_cache', response.data)

    def test_set_active_cache_driver_not_found(self):
        """Test setting an active cache driver that doesn't exist."""
        with patch('zi_coder_agent.cache_management.CacheToolMarketplace.set_active_driver') as mock_set:
            mock_set.return_value = False
            response = self.client.put('/api/cache/active/nonexistent')
            self.assertEqual(response.status_code, 404)
            self.assertIn(b'Driver nonexistent not found', response.data)

    def test_get_cache_value(self):
        """Test getting a cache value via API."""
        with patch('zi_coder_agent.cache_management.CacheToolMarketplace.get') as mock_get:
            mock_get.return_value = 'test_value'
            response = self.client.get('/api/cache/get/test_key')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'test_value', response.data)

    def test_get_cache_value_not_found(self):
        """Test getting a cache value that doesn't exist."""
        with patch('zi_coder_agent.cache_management.CacheToolMarketplace.get') as mock_get:
            mock_get.return_value = None
            response = self.client.get('/api/cache/get/test_key')
            self.assertEqual(response.status_code, 404)
            self.assertIn(b'Key not found or no active cache driver', response.data)

    def test_set_cache_value_missing_data(self):
        """Test setting a cache value with missing data."""
        response = self.client.post('/api/cache/set', json={})
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Missing key or value', response.data)

    def test_set_cache_value_failure(self):
        """Test setting a cache value with failure."""
        with patch('zi_coder_agent.cache_management.CacheToolMarketplace.set') as mock_set:
            mock_set.return_value = False
            response = self.client.post('/api/cache/set', json={
                'key': 'test_key',
                'value': 'test_value',
                'ttl': 3600
            })
            self.assertEqual(response.status_code, 400)
            self.assertIn(b'No active cache driver or set operation failed', response.data)

    def test_register_mcp_server_driver(self):
        """Test registering a new MCP server driver via API."""
        response = self.client.post('/api/mcp_servers/register', json={
            'name': 'mock_mcp',
            'driver_path': 'path.to.mock.mcp'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'MCP server driver mock_mcp registered', response.data)

    def test_register_mcp_server_driver_missing_data(self):
        """Test registering an MCP server driver with missing data."""
        response = self.client.post('/api/mcp_servers/register', json={})
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Missing name or driver_path', response.data)

    def test_set_active_mcp_server_driver(self):
        """Test setting an active MCP server driver via API."""
        self.client.post('/api/mcp_servers/register', json={
            'name': 'mock_mcp',
            'driver_path': 'path.to.mock.mcp'
        })
        with patch('zi_coder_agent.mcp_server_management.MCPServerMarketplace.set_active_driver') as mock_set:
            mock_set.return_value = True
            response = self.client.put('/api/mcp_servers/active/mock_mcp')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Active MCP server driver set to mock_mcp', response.data)

    def test_set_active_mcp_server_driver_not_found(self):
        """Test setting an active MCP server driver that doesn't exist."""
        with patch('zi_coder_agent.mcp_server_management.MCPServerMarketplace.set_active_driver') as mock_set:
            mock_set.return_value = False
            response = self.client.put('/api/mcp_servers/active/nonexistent')
            self.assertEqual(response.status_code, 404)
            self.assertIn(b'Driver nonexistent not found', response.data)

    def test_get_mcp_tools(self):
        """Test getting available tools from the active MCP server."""
        with patch('zi_coder_agent.mcp_server_management.MCPServerMarketplace.get_tools') as mock_get:
            mock_get.return_value = ['tool1', 'tool2']
            response = self.client.get('/api/mcp_servers/tools')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'tool1', response.data)
            self.assertIn(b'tool2', response.data)

    def test_get_mcp_tools_no_active_driver(self):
        """Test getting tools when no active MCP server driver is set."""
        with patch('zi_coder_agent.mcp_server_management.MCPServerMarketplace.get_tools') as mock_get:
            mock_get.return_value = None
            response = self.client.get('/api/mcp_servers/tools')
            self.assertEqual(response.status_code, 400)
            self.assertIn(b'No active MCP server driver', response.data)

    def test_get_mcp_resources(self):
        """Test getting available resources from the active MCP server."""
        with patch('zi_coder_agent.mcp_server_management.MCPServerMarketplace.get_resources') as mock_get:
            mock_get.return_value = ['resource1', 'resource2']
            response = self.client.get('/api/mcp_servers/resources')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'resource1', response.data)
            self.assertIn(b'resource2', response.data)

    def test_get_mcp_resources_no_active_driver(self):
        """Test getting resources when no active MCP server driver is set."""
        with patch('zi_coder_agent.mcp_server_management.MCPServerMarketplace.get_resources') as mock_get:
            mock_get.return_value = None
            response = self.client.get('/api/mcp_servers/resources')
            self.assertEqual(response.status_code, 400)
            self.assertIn(b'No active MCP server driver', response.data)

    def test_use_mcp_tool(self):
        """Test using a specific tool from the active MCP server."""
        with patch('zi_coder_agent.mcp_server_management.MCPServerMarketplace.use_tool') as mock_use:
            mock_use.return_value = 'tool_result'
            response = self.client.post('/api/mcp_servers/tool/test_tool', json={'arguments': {}})
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'tool_result', response.data)

    def test_use_mcp_tool_failure(self):
        """Test using a tool when no active MCP server driver is set or execution fails."""
        with patch('zi_coder_agent.mcp_server_management.MCPServerMarketplace.use_tool') as mock_use:
            mock_use.return_value = None
            response = self.client.post('/api/mcp_servers/tool/test_tool', json={'arguments': {}})
            self.assertEqual(response.status_code, 400)
            self.assertIn(b'No active MCP server driver or tool execution failed', response.data)

    def test_register_queue_driver(self):
        """Test registering a new queue driver via API."""
        response = self.client.post('/api/queue/register', json={
            'name': 'mock_queue',
            'driver_path': 'path.to.mock.queue'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Queue driver mock_queue registered', response.data)

    def test_register_queue_driver_missing_data(self):
        """Test registering a queue driver with missing data."""
        response = self.client.post('/api/queue/register', json={})
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Missing name or driver_path', response.data)

    def test_set_active_queue_driver(self):
        """Test setting an active queue driver via API."""
        self.client.post('/api/queue/register', json={
            'name': 'mock_queue',
            'driver_path': 'path.to.mock.queue'
        })
        with patch('zi_coder_agent.worker_management.QueueToolMarketplace.set_active_driver') as mock_set:
            mock_set.return_value = True
            response = self.client.put('/api/queue/active/mock_queue')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Active queue driver set to mock_queue', response.data)

    def test_set_active_queue_driver_not_found(self):
        """Test setting an active queue driver that doesn't exist."""
        with patch('zi_coder_agent.worker_management.QueueToolMarketplace.set_active_driver') as mock_set:
            mock_set.return_value = False
            response = self.client.put('/api/queue/active/nonexistent')
            self.assertEqual(response.status_code, 404)
            self.assertIn(b'Driver nonexistent not found', response.data)

    def test_enqueue_task(self):
        """Test enqueuing a task via API."""
        with patch('zi_coder_agent.worker_management.QueueToolMarketplace.enqueue_task') as mock_enqueue:
            mock_enqueue.return_value = 'task_123'
            response = self.client.post('/api/queue/enqueue', json={
                'task_name': 'test_task',
                'args': [],
                'kwargs': {}
            })
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'task_123', response.data)

    def test_enqueue_task_missing_data(self):
        """Test enqueuing a task with missing data."""
        response = self.client.post('/api/queue/enqueue', json={})
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Missing task_name', response.data)

    def test_enqueue_task_failure(self):
        """Test enqueuing a task with failure."""
        with patch('zi_coder_agent.worker_management.QueueToolMarketplace.enqueue_task') as mock_enqueue:
            mock_enqueue.return_value = None
            response = self.client.post('/api/queue/enqueue', json={
                'task_name': 'test_task',
                'args': [],
                'kwargs': {}
            })
            self.assertEqual(response.status_code, 400)
            self.assertIn(b'No active queue driver or enqueue failed', response.data)

    def test_get_task_status(self):
        """Test getting task status via API."""
        with patch('zi_coder_agent.worker_management.QueueToolMarketplace.get_task_status') as mock_status:
            mock_status.return_value = 'completed'
            response = self.client.get('/api/queue/status/task_123')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'completed', response.data)

    def test_get_task_status_not_found(self):
        """Test getting status for a task that doesn't exist."""
        with patch('zi_coder_agent.worker_management.QueueToolMarketplace.get_task_status') as mock_status:
            mock_status.return_value = None
            response = self.client.get('/api/queue/status/task_123')
            self.assertEqual(response.status_code, 404)
            self.assertIn(b'Task not found or no active queue driver', response.data)

    def test_connect_model_failure(self):
        """Test connecting to a model with failure."""
        with patch('zi_coder_agent.model_management.ModelMarketplace.connect') as mock_connect:
            mock_connect.return_value = False
            response = self.client.post('/api/models/connect')
            self.assertEqual(response.status_code, 400)
            self.assertIn(b'Failed to connect to model', response.data)

    def test_query_model_failure(self):
        """Test querying a model with failure."""
        with patch('zi_coder_agent.model_management.ModelMarketplace.query') as mock_query:
            mock_query.return_value = None
            response = self.client.post('/api/models/query', json={'input': 'test input'})
            self.assertEqual(response.status_code, 400)
            self.assertIn(b'No active model driver or query failed', response.data)

    def test_swagger_ui_endpoint(self):
        """Test accessing the Swagger UI endpoint."""
        response = self.client.get('/swagger', follow_redirects=True)
        if response.status_code != 200:
            response = self.client.get('/swagger/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Zi Coder Agent API', response.data)

if __name__ == '__main__':
    unittest.main()
