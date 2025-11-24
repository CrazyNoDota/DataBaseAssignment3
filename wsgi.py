import sys
import os

# Add the src directory to the Python path so that imports within src/app.py work correctly
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from app import app

if __name__ == "__main__":
    app.run()
