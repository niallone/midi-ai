import os
import asyncio
from app.src.api import create_api

# Create the Quart application by running the create_api function
# asyncio.run() is used because create_api is an async function
app = asyncio.run(create_api())

# This block is executed when the script is run directly (not imported)
if __name__ == "__main__":
    import hypercorn.asyncio
    
    # Create a Hypercorn configuration object
    config = hypercorn.Config()
    
    # Set the binding address and port
    # 0.0.0.0 means the server will be accessible from any network interface
    # 4050 is the port number the server will listen on
    config.bind = ["0.0.0.0:4050"]

    # Timeout configuration
    # 5 minutes (300 seconds) is the default timeout
    config.timeout = int(os.getenv('HYPERCORN_TIMEOUT', 300))
    
    # Run the Hypercorn ASGI server with our Quart app
    # hypercorn.asyncio.serve is an async function, so we use asyncio.run()
    asyncio.run(hypercorn.asyncio.serve(app, config))