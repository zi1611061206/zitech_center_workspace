"""
API Server Module

This module implements API endpoints using Flask to interact with all other components of the system.
It is designed with future extensibility in mind, following SOLID principles.
"""

from flask import Flask, jsonify, request
from flask_swagger_ui import get_swaggerui_blueprint
from typing import Optional
from ..model_management import ModelMarketplace
from ..mcp_server_management import MCPServerMarketplace
from ..cache_management import CacheToolMarketplace
from ..worker_management import QueueToolMarketplace
from ..database import DatabaseManager, get_db

def create_app() -> Flask:
    """
    Create and configure the Flask application.
    
    Returns:
        Flask: Configured Flask application instance.
    """
    app = Flask(__name__)
    
    # Initialize system components
    model_marketplace = ModelMarketplace()
    mcp_marketplace = MCPServerMarketplace()
    cache_marketplace = CacheToolMarketplace()
    queue_marketplace = QueueToolMarketplace()
    db_manager = DatabaseManager()
    
    # Swagger UI setup
    SWAGGER_URL = '/swagger'
    API_URL = '/static/swagger.json'
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "Zi Coder Agent API"
        }
    )
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
    
    # Connect to database on startup
    @app.before_request
    def initialize_system():
        """Initialize system components before the first request."""
        db_manager.connect()
        db_manager.create_all()
    
    # Close database connection on shutdown
    @app.teardown_appcontext
    def shutdown_system(exception=None):
        """Shutdown system components when the application context is torn down."""
        db_manager.disconnect()
    
    # API Endpoints for Model Management
    @app.route('/api/models/register', methods=['POST'])
    def register_model_driver():
        """Register a new model driver."""
        data = request.get_json()
        name = data.get('name')
        driver_path = data.get('driver_path')
        if not name or not driver_path:
            return jsonify({'error': 'Missing name or driver_path'}), 400
        
        # Dynamic import of driver class - placeholder for actual implementation
        # driver = import_driver(driver_path)
        # model_marketplace.register_driver(name, driver)
        return jsonify({'message': f'Model driver {name} registered'}), 200
    
    @app.route('/api/models/active/<string:name>', methods=['PUT'])
    def set_active_model_driver(name):
        """Set the active model driver."""
        if model_marketplace.set_active_driver(name):
            return jsonify({'message': f'Active model driver set to {name}'}), 200
        return jsonify({'error': f'Driver {name} not found'}), 404
    
    @app.route('/api/models/connect', methods=['POST'])
    def connect_model():
        """Connect to the active model driver."""
        if model_marketplace.connect():
            return jsonify({'message': 'Connected to model'}), 200
        return jsonify({'error': 'Failed to connect to model'}), 400
    
    @app.route('/api/models/query', methods=['POST'])
    def query_model():
        """Send a query to the active model driver."""
        data = request.get_json()
        input_data = data.get('input')
        if not input_data:
            return jsonify({'error': 'Missing input data'}), 400
        
        result = model_marketplace.query(input_data)
        if result is not None:
            return jsonify({'result': result}), 200
        return jsonify({'error': 'No active model driver or query failed'}), 400
    
    # API Endpoints for MCP Server Management
    @app.route('/api/mcp_servers/register', methods=['POST'])
    def register_mcp_server_driver():
        """Register a new MCP server driver."""
        data = request.get_json()
        name = data.get('name')
        driver_path = data.get('driver_path')
        if not name or not driver_path:
            return jsonify({'error': 'Missing name or driver_path'}), 400
        
        # Dynamic import of driver class - placeholder for actual implementation
        # driver = import_driver(driver_path)
        # mcp_marketplace.register_driver(name, driver)
        return jsonify({'message': f'MCP server driver {name} registered'}), 200
    
    @app.route('/api/mcp_servers/active/<string:name>', methods=['PUT'])
    def set_active_mcp_server_driver(name):
        """Set the active MCP server driver."""
        if mcp_marketplace.set_active_driver(name):
            return jsonify({'message': f'Active MCP server driver set to {name}'}), 200
        return jsonify({'error': f'Driver {name} not found'}), 404
    
    @app.route('/api/mcp_servers/tools', methods=['GET'])
    def get_mcp_tools():
        """Get available tools from the active MCP server."""
        tools = mcp_marketplace.get_tools()
        if tools is not None:
            return jsonify({'tools': tools}), 200
        return jsonify({'error': 'No active MCP server driver'}), 400
    
    @app.route('/api/mcp_servers/resources', methods=['GET'])
    def get_mcp_resources():
        """Get available resources from the active MCP server."""
        resources = mcp_marketplace.get_resources()
        if resources is not None:
            return jsonify({'resources': resources}), 200
        return jsonify({'error': 'No active MCP server driver'}), 400
    
    @app.route('/api/mcp_servers/tool/<string:tool_name>', methods=['POST'])
    def use_mcp_tool(tool_name):
        """Use a specific tool from the active MCP server."""
        data = request.get_json()
        arguments = data.get('arguments', {})
        result = mcp_marketplace.use_tool(tool_name, arguments)
        if result is not None:
            return jsonify({'result': result}), 200
        return jsonify({'error': 'No active MCP server driver or tool execution failed'}), 400
    
    # API Endpoints for Cache Management
    @app.route('/api/cache/register', methods=['POST'])
    def register_cache_driver():
        """Register a new cache driver."""
        data = request.get_json()
        name = data.get('name')
        driver_path = data.get('driver_path')
        if not name or not driver_path:
            return jsonify({'error': 'Missing name or driver_path'}), 400
        
        # Dynamic import of driver class - placeholder for actual implementation
        # driver = import_driver(driver_path)
        # cache_marketplace.register_driver(name, driver)
        return jsonify({'message': f'Cache driver {name} registered'}), 200
    
    @app.route('/api/cache/active/<string:name>', methods=['PUT'])
    def set_active_cache_driver(name):
        """Set the active cache driver."""
        if cache_marketplace.set_active_driver(name):
            return jsonify({'message': f'Active cache driver set to {name}'}), 200
        return jsonify({'error': f'Driver {name} not found'}), 404
    
    @app.route('/api/cache/set', methods=['POST'])
    def set_cache_value():
        """Set a value in the cache."""
        data = request.get_json()
        key = data.get('key')
        value = data.get('value')
        ttl = data.get('ttl')
        if not key or value is None:
            return jsonify({'error': 'Missing key or value'}), 400
        
        if cache_marketplace.set(key, value, ttl):
            return jsonify({'message': f'Cache value set for key {key}'}), 200
        return jsonify({'error': 'No active cache driver or set operation failed'}), 400
    
    @app.route('/api/cache/get/<string:key>', methods=['GET'])
    def get_cache_value(key):
        """Get a value from the cache."""
        value = cache_marketplace.get(key)
        if value is not None:
            return jsonify({'value': value}), 200
        return jsonify({'error': 'Key not found or no active cache driver'}), 404
    
    # API Endpoints for Worker Management
    @app.route('/api/queue/register', methods=['POST'])
    def register_queue_driver():
        """Register a new queue driver."""
        data = request.get_json()
        name = data.get('name')
        driver_path = data.get('driver_path')
        if not name or not driver_path:
            return jsonify({'error': 'Missing name or driver_path'}), 400
        
        # Dynamic import of driver class - placeholder for actual implementation
        # driver = import_driver(driver_path)
        # queue_marketplace.register_driver(name, driver)
        return jsonify({'message': f'Queue driver {name} registered'}), 200
    
    @app.route('/api/queue/active/<string:name>', methods=['PUT'])
    def set_active_queue_driver(name):
        """Set the active queue driver."""
        if queue_marketplace.set_active_driver(name):
            return jsonify({'message': f'Active queue driver set to {name}'}), 200
        return jsonify({'error': f'Driver {name} not found'}), 404
    
    @app.route('/api/queue/enqueue', methods=['POST'])
    def enqueue_task():
        """Enqueue a task for processing."""
        data = request.get_json()
        task_name = data.get('task_name')
        args = data.get('args', [])
        kwargs = data.get('kwargs', {})
        if not task_name:
            return jsonify({'error': 'Missing task_name'}), 400
        
        task_id = queue_marketplace.enqueue_task(task_name, args, kwargs)
        if task_id:
            return jsonify({'task_id': task_id}), 200
        return jsonify({'error': 'No active queue driver or enqueue failed'}), 400
    
    @app.route('/api/queue/status/<string:task_id>', methods=['GET'])
    def get_task_status(task_id):
        """Get the status of a task."""
        status = queue_marketplace.get_task_status(task_id)
        if status is not None:
            return jsonify({'status': status}), 200
        return jsonify({'error': 'Task not found or no active queue driver'}), 404
    
    return app

# Placeholder for dynamic driver import - to be implemented based on driver_path
def import_driver(driver_path: str) -> Optional[type]:
    """
    Dynamically import a driver class based on the provided path.
    Placeholder for actual implementation.
    
    Args:
        driver_path: Path to the driver class (e.g., 'module.submodule.MyDriverClass')
        
    Returns:
        Optional[type]: The driver class if imported successfully, None otherwise.
    """
    # Implementation would use importlib to dynamically load the class
    return None
