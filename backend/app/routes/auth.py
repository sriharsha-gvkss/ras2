from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import Optional
import jwt
from datetime import datetime, timedelta
import hashlib

router = APIRouter(prefix="/auth", tags=["Authentication"])
security = HTTPBearer()

# Secret key for JWT (in production, use environment variable)
SECRET_KEY = "your-secret-key-here"
ALGORITHM = "HS256"

# Demo users (in production, use database)
DEMO_USERS = {
    "user": {
        "username": "user",
        "password_hash": hashlib.sha256("user123".encode()).hexdigest(),
        "role": "user"
    },
    "admin": {
        "username": "admin", 
        "password_hash": hashlib.sha256("admin123".encode()).hexdigest(),
        "role": "admin"
    }
}

class UserLogin(BaseModel):
    username: str
    password: str

class UserRegister(BaseModel):
    username: str
    password: str
    email: str
    role: str = "user"

class Token(BaseModel):
    access_token: str
    token_type: str
    role: str

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@router.post("/login", response_model=Token)
async def login(user_credentials: UserLogin):
    username = user_credentials.username
    password = user_credentials.password
    
    # Check if user exists
    if username not in DEMO_USERS:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    user = DEMO_USERS[username]
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    
    if password_hash != user["password_hash"]:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Create access token
    access_token_expires = timedelta(hours=24)
    access_token = create_access_token(
        data={"sub": username, "role": user["role"]}, 
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "role": user["role"]
    }

@router.post("/register")
async def register(user_data: UserRegister):
    # Check if username already exists
    if user_data.username in DEMO_USERS:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    # In a real app, you would save to database
    # For demo, we'll just return success
    return {"message": "Registration successful", "username": user_data.username}

@router.get("/me")
async def get_current_user(username: str = Depends(verify_token)):
    if username not in DEMO_USERS:
        raise HTTPException(status_code=404, detail="User not found")
    
    user = DEMO_USERS[username]
    return {
        "username": username,
        "role": user["role"]
    }

@router.get("/validate")
async def validate_token(username: str = Depends(verify_token)):
    return {"valid": True, "username": username} 