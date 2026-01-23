#!/usr/bin/env python3
import os
import sys
from pathlib import Path

# Add the eggs module to the path
sys.path.insert(0, str(Path(__file__).parent))

# Import the original main function
from eggs.main import main as original_main


def main():
    # Check if we're running the API or the original CLI
    if len(sys.argv) > 1 and sys.argv[1] == "api":
        # Run the FastAPI server
        import uvicorn
        from eggs.api import app

        # Get port from environment or default to 8000
        port = int(os.environ.get("PORT", 8000))

        uvicorn.run(app, host="0.0.0.0", port=port)
    else:
        # Run the original CLI functionality
        original_main()


if __name__ == "__main__":
    main()
