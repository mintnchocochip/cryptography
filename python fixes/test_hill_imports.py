#!/usr/bin/env python3
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
