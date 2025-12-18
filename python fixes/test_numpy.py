#!/usr/bin/env python3
"""
Simple test script to verify numpy installation and basic functionality.
This helps diagnose import issues with numpy.
"""

import sys


def test_numpy_import():
    """Test if numpy can be imported successfully."""
    try:
        import numpy as np

        print("✓ SUCCESS: numpy imported successfully")
        print(f"  - numpy version: {np.__version__}")
        print(f"  - numpy location: {np.__file__}")
        return True
    except ImportError as e:
        print("✗ FAILED: Could not import numpy")
        print(f"  - Error: {e}")
        return False


def test_numpy_basic_operations():
    """Test basic numpy operations."""
    try:
        import numpy as np

        # Test array creation
        arr1 = np.array([1, 2, 3])
        arr2 = np.array([[1, 2], [3, 4]])

        print("✓ SUCCESS: Array creation works")
        print(f"  - 1D array: {arr1}")
        print(f"  - 2D array:\n{arr2}")

        # Test matrix operations (needed for Hill cipher)
        matrix_a = np.array([[1, 2], [3, 4]])
        matrix_b = np.array([[5, 6], [7, 8]])
        result = matrix_a @ matrix_b

        print("✓ SUCCESS: Matrix multiplication works")
        print(f"  - Result: \n{result}")

        # Test determinant (needed for Hill cipher decryption)
        det = np.linalg.det(matrix_a)
        print(f"✓ SUCCESS: Determinant calculation works: {det}")

        return True

    except Exception as e:
        print("✗ FAILED: Error in numpy operations")
        print(f"  - Error: {e}")
        return False


def main():
    """Run all numpy tests."""
    print("=" * 50)
    print("NUMPY INSTALLATION TEST")
    print("=" * 50)

    print(f"Python version: {sys.version}")
    print(f"Python executable: {sys.executable}")
    print()

    # Test import
    import_success = test_numpy_import()
    print()

    if import_success:
        # Test operations
        operations_success = test_numpy_basic_operations()
        print()

        if operations_success:
            print("🎉 ALL TESTS PASSED! numpy is working correctly.")
        else:
            print("⚠️  Import works but operations failed.")
    else:
        print("❌ numpy is not installed or not accessible.")
        print("\nTo fix this, try:")
        print("  python -m pip install numpy")
        print("  or")
        print("  pip install numpy")


if __name__ == "__main__":
    main()
