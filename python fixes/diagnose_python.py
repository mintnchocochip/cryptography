#!/usr/bin/env python3
"""
Comprehensive Python Environment Diagnostic Script
This script helps identify and fix numpy import issues by checking all Python installations.
"""

import json
import os
import subprocess
import sys
from pathlib import Path


def run_command(cmd):
    """Run a command and return its output."""
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, timeout=10
        )
        return result.returncode, result.stdout.strip(), result.stderr.strip()
    except subprocess.TimeoutExpired:
        return -1, "", "Command timed out"
    except Exception as e:
        return -1, "", str(e)


def check_python_executable(python_cmd):
    """Check a specific Python executable for numpy."""
    print(f"\n{'=' * 60}")
    print(f"CHECKING: {python_cmd}")
    print(f"{'=' * 60}")

    # Get Python info
    code, version_out, version_err = run_command(f"{python_cmd} --version")
    if code != 0:
        print(f"❌ Failed to run {python_cmd}: {version_err}")
        return False

    print(f"✓ Version: {version_out}")

    # Get executable path
    code, exec_out, exec_err = run_command(
        f'{python_cmd} -c "import sys; print(sys.executable)"'
    )
    if code != 0:
        print(f"❌ Failed to get executable path: {exec_err}")
        return False

    print(f"✓ Executable: {exec_out}")

    # Check if numpy is installed
    code, numpy_out, numpy_err = run_command(
        f"{python_cmd} -c \"import numpy; print(f'numpy {numpy.__version__} at {numpy.__file__}')\""
    )
    if code != 0:
        print(f"❌ numpy NOT FOUND: {numpy_err}")
        print(f"   Installing numpy...")

        # Try to install numpy
        install_code, install_out, install_err = run_command(
            f"{python_cmd} -m pip install numpy"
        )
        if install_code != 0:
            print(f"❌ Failed to install numpy: {install_err}")
            return False
        else:
            print(f"✓ numpy installed successfully")
            # Verify installation
            code, numpy_out, numpy_err = run_command(
                f"{python_cmd} -c \"import numpy; print(f'numpy {numpy.__version__} at {numpy.__file__}')\""
            )
            if code == 0:
                print(f"✓ {numpy_out}")
                return True
            else:
                print(f"❌ Still can't import numpy after installation: {numpy_err}")
                return False
    else:
        print(f"✓ {numpy_out}")
        return True


def find_all_python_installations():
    """Find all Python installations on the system."""
    python_executables = []

    # Common Python commands
    common_commands = ["python", "python3", "py", "python.exe", "python3.exe"]

    # Check common commands
    for cmd in common_commands:
        code, out, err = run_command(f"where {cmd}")
        if code == 0:
            for path in out.split("\n"):
                if path.strip() and path.strip() not in python_executables:
                    python_executables.append(path.strip())

    # Check Python Launcher
    code, out, err = run_command("py -0")
    if code == 0:
        print(f"Python Launcher found versions:\n{out}")
        # Extract version numbers and test them
        for line in out.split("\n"):
            if "Python" in line and ("3.1" in line):
                version = line.split()[0].replace("-V:", "").replace("*", "").strip()
                if version:
                    python_executables.append(f"py -{version}")

    # Check common installation paths
    common_paths = [
        "C:\\Python313\\python.exe",
        "C:\\Python312\\python.exe",
        "C:\\Python311\\python.exe",
        "C:\\Program Files\\Python313\\python.exe",
        "C:\\Program Files\\Python312\\python.exe",
        "C:\\Program Files\\Python311\\python.exe",
        os.path.expanduser(
            "~\\AppData\\Local\\Programs\\Python\\Python313\\python.exe"
        ),
        os.path.expanduser(
            "~\\AppData\\Local\\Programs\\Python\\Python312\\python.exe"
        ),
        os.path.expanduser(
            "~\\AppData\\Local\\Programs\\Python\\Python311\\python.exe"
        ),
        os.path.expanduser("~\\AppData\\Local\\Microsoft\\WindowsApps\\python.exe"),
    ]

    for path in common_paths:
        if os.path.exists(path) and path not in python_executables:
            python_executables.append(path)

    return list(set(python_executables))  # Remove duplicates


def create_test_script():
    """Create a test script to verify numpy import."""
    test_script = """
import sys
print(f"Python executable: {sys.executable}")
print(f"Python version: {sys.version}")

try:
    import numpy as np
    print(f"✓ SUCCESS: numpy {np.__version__} imported from {np.__file__}")

    # Test basic functionality
    arr = np.array([[1, 2], [3, 4]])
    det = np.linalg.det(arr)
    print(f"✓ Matrix operations work: determinant = {det}")

except ImportError as e:
    print(f"❌ FAILED: {e}")
except Exception as e:
    print(f"❌ ERROR: {e}")
"""

    with open("numpy_test.py", "w") as f:
        f.write(test_script)

    return "numpy_test.py"


def main():
    """Main diagnostic function."""
    print("🔍 PYTHON & NUMPY DIAGNOSTIC TOOL")
    print("=" * 80)

    # System information
    print(f"Operating System: {os.name}")
    print(f"Current Working Directory: {os.getcwd()}")
    print(f"PATH: {os.environ.get('PATH', 'Not found')[:200]}...")

    # Find all Python installations
    print(f"\n📋 FINDING ALL PYTHON INSTALLATIONS...")
    python_executables = find_all_python_installations()

    print(f"Found {len(python_executables)} Python executables:")
    for i, exe in enumerate(python_executables, 1):
        print(f"  {i}. {exe}")

    if not python_executables:
        print("❌ No Python installations found!")
        return

    # Test each Python installation
    working_pythons = []
    failed_pythons = []

    for python_exe in python_executables:
        try:
            if check_python_executable(python_exe):
                working_pythons.append(python_exe)
            else:
                failed_pythons.append(python_exe)
        except Exception as e:
            print(f"❌ Error checking {python_exe}: {e}")
            failed_pythons.append(python_exe)

    # Summary
    print(f"\n{'=' * 80}")
    print("📊 SUMMARY")
    print(f"{'=' * 80}")

    print(f"✅ Working Python installations with numpy ({len(working_pythons)}):")
    for python_exe in working_pythons:
        print(f"   • {python_exe}")

    if failed_pythons:
        print(f"\n❌ Failed Python installations ({len(failed_pythons)}):")
        for python_exe in failed_pythons:
            print(f"   • {python_exe}")

    # Create test script
    test_file = create_test_script()
    print(f"\n🧪 CREATED TEST SCRIPT: {test_file}")
    print("Run this with any Python to test numpy:")
    if working_pythons:
        print(f"   {working_pythons[0]} {test_file}")

    # Recommendations
    print(f"\n💡 RECOMMENDATIONS:")
    if working_pythons:
        print(f"1. Use this Python command for your projects: {working_pythons[0]}")
        print(f"2. Always use the full command when installing packages:")
        print(f"   {working_pythons[0]} -m pip install package_name")
        print(f"3. Run your scripts with: {working_pythons[0]} script_name.py")
    else:
        print("1. No working Python with numpy found!")
        print("2. Try installing numpy manually:")
        print("   python -m pip install numpy")
        print("   or")
        print("   py -3.13 -m pip install numpy")

    # IDE Configuration
    print(f"\n⚙️  IDE CONFIGURATION:")
    print("If using VS Code:")
    print("1. Press Ctrl+Shift+P")
    print("2. Type 'Python: Select Interpreter'")
    print(
        f"3. Choose: {working_pythons[0] if working_pythons else 'C:\\Python313\\python.exe'}"
    )

    print("\nIf using PyCharm:")
    print("1. Go to File → Settings → Project → Python Interpreter")
    print(
        f"2. Set interpreter to: {working_pythons[0] if working_pythons else 'C:\\Python313\\python.exe'}"
    )

    return len(working_pythons) > 0


if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎉 DIAGNOSTIC COMPLETE - At least one working Python found!")
    else:
        print("\n💥 DIAGNOSTIC COMPLETE - Issues found that need fixing!")
