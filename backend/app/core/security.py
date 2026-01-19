from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
import os
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
from pathlib import Path

# Explicitly load backend/.env if not already loaded
base_dir = Path(__file__).resolve().parents[2]
env_path = base_dir / '.env'
if env_path.exists():
    load_dotenv(env_path)
else:
    load_dotenv()

# Reuse secret from env or default
SECRET_KEY = os.getenv("SECRET_KEY", "justwrite-secret")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 3000

# Using pbkdf2_sha256 instead of bcrypt to avoid Windows-specific 72-byte limit bugs in passlib
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
