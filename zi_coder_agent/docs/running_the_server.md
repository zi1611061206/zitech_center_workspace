# Running the Zi Coder Agent Server

This guide provides instructions for running the `zi-coder-agent` server and accessing the API documentation via Swagger UI.

## Prerequisites

- **Virtual Environment**: Ensure you have set up a virtual environment and installed the dependencies as described in [Virtual Environment Setup](virtual_environment_setup.md).

## Starting the Server

1. **Activate the Virtual Environment**:
   If you haven't already activated your virtual environment, do so now:

   - On Windows:
     ```bash
     .venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source .venv/bin/activate
     ```

2. **Run the Server**:
   Use the provided `run_server.py` script to start the Flask server:

   ```bash
   python run_server.py
   ```

   By default, the server will run on `http://127.0.0.1:5000/`. You should see output in your terminal indicating that the server is running.

## Accessing the Swagger UI

The `zi-coder-agent` API provides a Swagger UI for interactive API documentation. Once the server is running, you can access the Swagger UI at:

[http://127.0.0.1:5000/swagger](http://127.0.0.1:5000/swagger)

This interface allows you to explore the API endpoints, view their documentation, and even test API calls directly from the browser.

## Stopping the Server

To stop the server, simply press `Ctrl+C` in the terminal where the server is running. This will terminate the Flask application.

## Additional Notes

- **Server Configuration**: If you need to change the host or port, you can modify the `run_server.py` script or pass arguments when running the script. Check the script for more details on configuration options.
- **Troubleshooting**: If you encounter issues, ensure all dependencies are installed correctly and that no other application is using the port (default is 5000).

By following these steps, you can easily run the `zi-coder-agent` server and interact with its API through the Swagger UI.
