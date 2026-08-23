from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import jwt
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError

import models
import schemas
from database import get_db

# JWT কনফিগারেশন 
SECRET_KEY = "phitron-mid-term-super-secret-key" # প্রোডাকশনে এটি পরিবর্তন করে নিরাপদ কিছু দিতে হবে
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
router = APIRouter(prefix="/auth", tags=["Authentication"])

# পাসওয়ার্ড হ্যাশ এবং ভেরিফাই করার ফাংশন
def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# JWT টোকেন তৈরির ফাংশন
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# ==========================
# 1. User Registration[cite: 1]
# ==========================
@router.post("/register", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # ইউজারনেম বা ইমেইল আগে থেকেই আছে কিনা চেক করা
    db_user = db.query(models.User).filter(
        (models.User.username == user.username) | (models.User.email == user.email)
    ).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username or Email already registered")
    
    # ডেটাবেসে সেভ করার আগে পাসওয়ার্ড হ্যাশ করা[cite: 1]
    hashed_password = get_password_hash(user.password)
    
    # ডেটাবেসে ইউজার ইনফরমেশন সেভ করা[cite: 1]
    new_user = models.User(
        username=user.username, 
        email=user.email, 
        hashed_password=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # রেসপন্সে হ্যাশড পাসওয়ার্ড রিটার্ন করা হবে না কারণ আমরা response_model=schemas.UserResponse ব্যবহার করেছি[cite: 1]
    return new_user 

# ==========================
# 2. User Login[cite: 1]
# ==========================
@router.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # ডেটাবেস থেকে ইউজারনেম এবং পাসওয়ার্ড ভেরিফাই করা[cite: 1]
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # সফলভাবে ভেরিফাই হওয়ার পর JWT অ্যাক্সেস টোকেন তৈরি করা[cite: 1]
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    
    # অ্যাক্সেস টোকেন এবং টোকেন টাইপ রিটার্ন করা[cite: 1]
    return {"access_token": access_token, "token_type": "bearer"}


# টোকেন গ্রহণ করার জন্য স্কিম
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# বর্তমান লগ-ইন করা ইউজারকে বের করার ফাংশন
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id_str: str = payload.get("sub")
        if user_id_str is None:
            raise credentials_exception
        token_data = int(user_id_str)
    except (JWTError, ValueError):
        raise credentials_exception
        
    user = db.query(models.User).filter(models.User.id == token_data).first()
    if user is None:
        raise credentials_exception
    return user