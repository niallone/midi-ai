import sys
import os

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.main import create_app

app = create_app()

if __name__ == '__main__':
    # Create the application instance
    app = create_app()
    
    # Run the application
    # The host '0.0.0.0' makes the server externally visible
    app.run(host='0.0.0.0', port=4050)