import subprocess
import sys
from pathlib import Path


def test_hello_world_no_args():
    """Test hello world with no arguments"""
    result = subprocess.run(
        [sys.executable, str(Path(__file__).parent.parent / "eggs" / "main.py")],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    # Should contain the username
    assert "Hello" in result.stdout


def test_hello_world_with_args():
    """Test hello world with arguments"""
    result = subprocess.run(
        [
            sys.executable,
            str(Path(__file__).parent.parent / "eggs" / "main.py"),
            "World",
        ],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert "Hello World" in result.stdout


def test_hello_world_multiple_args():
    """Test hello world with multiple arguments"""
    result = subprocess.run(
        [
            sys.executable,
            str(Path(__file__).parent.parent / "eggs" / "main.py"),
            "World",
            "Python",
        ],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert "Hello World Python" in result.stdout
