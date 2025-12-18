#!/usr/bin/env python3
"""
Crypto Project Environment Setup Script
========================================

This script ensures that all required packages are installed correctly
and helps prevent future import issues with numpy and other dependencies.

Usage:
    python setup_environment.py

This will:
1. Check your Python installation
2. Install all required packages
3. Verify all imports work correctly
4. Provide instructions for your IDE setup
"""

import os
import subprocess
import sys
from pathlib import Path


def run_command(cmd, description=""):
    """Run a command and handle errors gracefully."""
    print(f"🔄 {description}")
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, check=True
        )
        print(f"✅ Success!")
        if result.stdout.strip():
            print(f"   Output: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed: {e}")
        if e.stdout:
            print(f"   Output: {e.stdout}")
        if e.stderr:
            print(f"   Error: {e.stderr}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False


def check_python_version():
    """Check if we're using a compatible Python version."""
    print(f"🐍 Python Version Check")
    print(f"   Version: {sys.version}")
    print(f"   Executable: {sys.executable}")

    version_info = sys.version_info
    if version_info.major < 3 or (version_info.major == 3 and version_info.minor < 8):
        print("❌ Python 3.8 or higher is required!")
        return False

    print("✅ Python version is compatible")
    return True


def install_packages():
    """Install all required packages for the crypto project."""
    packages = [
        ("numpy", "Numerical computing library"),
        ("sympy", "Symbolic mathematics library"),
    ]

    print(f"\n📦 Installing Required Packages")
    print(f"=" * 50)

    all_success = True
    python_cmd = sys.executable

    for package, description in packages:
        print(f"\n📋 Installing {package} ({description})")

        # First try to import to see if already installed
        try:
            __import__(package)
            print(f"✅ {package} is already installed")
            continue
        except ImportError:
            pass

        # Install the package
        cmd = f'"{python_cmd}" -m pip install {package} --user'
        success = run_command(cmd, f"Installing {package}")

        if success:
            # Verify installation
            try:
                __import__(package)
                print(f"✅ {package} installed and verified successfully")
            except ImportError:
                print(f"❌ {package} was installed but can't be imported")
                all_success = False
        else:
            all_success = False

    return all_success


def test_imports():
    """Test all imports required for the crypto project."""
    print(f"\n🧪 Testing All Imports")
    print(f"=" * 50)

    tests = [
        ("import numpy as np", "NumPy"),
        ("import sympy", "SymPy"),
        ("from sympy import Matrix", "SymPy Matrix"),
        ("import socket", "Socket (built-in)"),
        ("import os", "OS (built-in)"),
    ]

    all_success = True

    for test_code, description in tests:
        try:
            exec(test_code)
            print(f"✅ {description}: OK")
        except Exception as e:
            print(f"❌ {description}: FAILED - {e}")
            all_success = False

    return all_success


def test_crypto_functionality():
    """Test specific functionality needed for crypto operations."""
    print(f"\n🔐 Testing Crypto Functionality")
    print(f"=" * 50)

    try:
        # Test numpy matrix operations (needed for Hill cipher)
        import numpy as np

        matrix_a = np.array([[1, 2], [3, 4]])
        matrix_b = np.array([[5, 6], [7, 8]])
        result = matrix_a @ matrix_b
        det = np.linalg.det(matrix_a)
        print(f"✅ NumPy matrix operations: OK (det = {det:.2f})")

        # Test sympy matrix operations (needed for Hill cipher inverse)
        from sympy import Matrix

        sym_matrix = Matrix([[1, 2], [3, 4]])
        sym_det = sym_matrix.det()
        sym_adj = sym_matrix.adjugate()
        print(f"✅ SymPy matrix operations: OK (symbolic det = {sym_det})")

        # Test socket operations (needed for client-server)
        import socket

        s = socket.socket()
        s.close()
        print(f"✅ Socket operations: OK")

        return True

    except Exception as e:
        print(f"❌ Crypto functionality test failed: {e}")
        return False


def create_test_files():
    """Create test files for each cipher type."""
    print(f"\n📄 Creating Test Files")
    print(f"=" * 50)

    # Create a simple test script for each cipher
    test_scripts = {
        "test_hill_imports.py": '''#!/usr/bin/env python3
"""Test Hill Cipher Imports"""
import sys
print(f"Python: {sys.executable}")

try:
    import numpy as np
    print(f"✅ NumPy {np.__version__}")

    from sympy import Matrix
    print(f"✅ SymPy Matrix")

    import socket
    print(f"✅ Socket")

    # Test basic Hill cipher operations
    key_matrix = np.array([[6, 24], [13, 16]])
    test_vector = np.array([0, 2])  # 'ac'
    result = test_vector @ key_matrix % 26
    print(f"✅ Matrix multiplication works: {result}")

    print("🎉 All Hill cipher dependencies are working!")

except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)
''',
        "test_basic_crypto.py": '''#!/usr/bin/env python3
"""Test Basic Crypto Operations"""

def test_caesar():
    """Test Caesar cipher logic"""
    def caesar_encrypt(text, shift):
        result = ""
        for char in text.upper():
            if char.isalpha():
                result += chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
            else:
                result += char
        return result

    encrypted = caesar_encrypt("HELLO", 3)
    expected = "KHOOR"
    assert encrypted == expected, f"Expected {expected}, got {encrypted}"
    print("✅ Caesar cipher test passed")

def test_vigenere():
    """Test Vigenere cipher logic"""
    def vigenere_encrypt(text, key):
        result = ""
        key = key.upper()
        key_index = 0

        for char in text.upper():
            if char.isalpha():
                shift = ord(key[key_index % len(key)]) - ord('A')
                encrypted_char = chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
                result += encrypted_char
                key_index += 1
            else:
                result += char
        return result

    encrypted = vigenere_encrypt("HELLO", "KEY")
    print(f"✅ Vigenere cipher test: HELLO -> {encrypted}")

if __name__ == "__main__":
    test_caesar()
    test_vigenere()
    print("🎉 All basic crypto tests passed!")
''',
    }

    for filename, content in test_scripts.items():
        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"✅ Created {filename}")
        except Exception as e:
            print(f"❌ Failed to create {filename}: {e}")


def show_usage_instructions():
    """Show instructions for using the correct Python command."""
    print(f"\n📚 Usage Instructions")
    print(f"=" * 50)

    python_cmd = sys.executable
    print(f"✅ Your working Python command: {python_cmd}")
    print(f"\n🔧 To avoid future issues, always use:")
    print(f"   Installation: {python_cmd} -m pip install package_name")
    print(f"   Run scripts:  {python_cmd} script_name.py")
    print(f"   Or use:       py -3.13 script_name.py")

    print(f"\n💡 IDE Configuration:")
    print(f"   VS Code: Ctrl+Shift+P -> 'Python: Select Interpreter'")
    print(f"           Choose: {python_cmd}")
    print(f"   PyCharm: File -> Settings -> Project -> Python Interpreter")
    print(f"            Set to: {python_cmd}")

    print(f"\n🏃 Quick Test Commands:")
    print(f"   py -3.13 test_hill_imports.py")
    print(f"   py -3.13 test_basic_crypto.py")


def main():
    """Main setup function."""
    print("🚀 CRYPTO PROJECT ENVIRONMENT SETUP")
    print("=" * 60)
    print("This script will set up your Python environment for crypto projects")
    print("=" * 60)

    # Step 1: Check Python version
    if not check_python_version():
        print("\n❌ Setup failed: Incompatible Python version")
        return False

    # Step 2: Install packages
    if not install_packages():
        print("\n❌ Setup failed: Package installation issues")
        return False

    # Step 3: Test imports
    if not test_imports():
        print("\n❌ Setup failed: Import test issues")
        return False

    # Step 4: Test crypto functionality
    if not test_crypto_functionality():
        print("\n❌ Setup failed: Crypto functionality issues")
        return False

    # Step 5: Create test files
    create_test_files()

    # Step 6: Show usage instructions
    show_usage_instructions()

    print(f"\n🎉 SETUP COMPLETE!")
    print("=" * 60)
    print("Your environment is now ready for crypto programming!")
    print("All required packages are installed and tested.")
    print("=" * 60)

    return True


if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⏹️ Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Unexpected error during setup: {e}")
        sys.exit(1)
