#!/usr/bin/env python3
import os
import sys
from pathlib import Path


def main():
    if len(sys.argv) > 1:
        # Print "Hello " followed by the parameters
        print("Hello " + " ".join(sys.argv[1:]))
    else:
        # Print the current user's username
        username = os.getlogin()
        print(f"Hello {username}")


if __name__ == "__main__":
    main()
