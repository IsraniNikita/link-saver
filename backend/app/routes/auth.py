from fastapi import APIRouter, HTTPException
from app.models import UserCreate, UserLogin
from app.database import users_collection
from jose import jwt
from dotenv import load_dotenv
import os
import bcrypt

load_dotenv()
router = APIRouter()
JWT_SECRET = os.getenv("JWT_SECRET")

def create_token(email: str):
    return jwt.encode({"email": email}, JWT_SECRET, algorithm="HS256")

@router.post("/signup")
def signup(user: UserCreate):
    if users_collection.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_pw = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    users_collection.insert_one({"email": user.email, "password": hashed_pw})
    return {"message": "User created successfully"}

@router.post("/login")
def login(user: UserLogin):
    db_user = users_collection.find_one({"email": user.email})
    if not db_user or not bcrypt.checkpw(user.password.encode('utf-8'), db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_token(user.email)
    return {"access_token": token}
