#!/usr/bin/env python3

import sys
import getpass


def main():
    if len(sys.argv) > 1:
        # Print "Hello " followed by the parameters
        print("Hello " + " ".join(sys.argv[1:]))
    else:
        # Print the current user's username
        username = getpass.getuser()
        print(f"Hello {username}")


if __name__ == "__main__":
    main()
