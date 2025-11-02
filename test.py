# test_hash.py
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Test hashing
password = "mypass123"
print(f"Original password: {password}")
print(f"Password length: {len(password)} chars, {len(password.encode('utf-8'))} bytes")

try:
    hashed = pwd_context.hash(password)
    print(f"✅ Hashed successfully: {hashed[:50]}...")
    
    # Test verification
    is_valid = pwd_context.verify(password, hashed)
    print(f"✅ Verification: {is_valid}")
except Exception as e:
    print(f"❌ Error: {e}")