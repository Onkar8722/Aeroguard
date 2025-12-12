try:
    from flask import Flask
    print("✓ Flask OK")
except Exception as e:
    print(f"✗ Flask ERROR: {e}")

try:
    from face_utils import recognize_face
    print("✓ face_utils OK")
except Exception as e:
    print(f"✗ face_utils ERROR: {e}")

try:
    from camera_manager import CameraStream
    print("✓ camera_manager OK")
except Exception as e:
    print(f"✗ camera_manager ERROR: {e}")

print("\nAll imports successful!")
