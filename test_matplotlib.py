#!/usr/bin/env python3
"""
Test matplotlib animation import
"""

print("Testing matplotlib imports...")

try:
    import matplotlib
    print(f"✅ matplotlib version: {matplotlib.__version__}")
    print(f"✅ matplotlib location: {matplotlib.__file__}")
except ImportError as e:
    print(f"❌ Failed to import matplotlib: {e}")
    exit(1)

try:
    import matplotlib.pyplot as plt
    print("✅ matplotlib.pyplot imported successfully")
except ImportError as e:
    print(f"❌ Failed to import matplotlib.pyplot: {e}")
    exit(1)

try:
    import matplotlib.animation
    print("✅ matplotlib.animation module imported successfully")
    print(f"✅ animation module location: {matplotlib.animation.__file__}")
except ImportError as e:
    print(f"❌ Failed to import matplotlib.animation: {e}")
    exit(1)

try:
    from matplotlib.animation import FuncAnimation
    print("✅ FuncAnimation imported successfully")
    print(f"✅ FuncAnimation class: {FuncAnimation}")
except ImportError as e:
    print(f"❌ Failed to import FuncAnimation: {e}")
    print("This suggests the animation module is corrupted or incomplete")
    exit(1)

print("\n🎉 All matplotlib imports successful!")
print("You can now run the Earth-Moon simulation.")
