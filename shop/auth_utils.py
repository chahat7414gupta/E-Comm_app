
from django.contrib.auth.hashers import make_password, check_password
from django.middleware import csrf
from django.contrib import messages
from django.http import HttpRequest
from .db import SessionLocal
from .models_sa import User

def get_current_user(request: HttpRequest):
    user_id = request.session.get('user_id')
    if not user_id:
        return None
    db = SessionLocal()
    try:
        return db.get(User, user_id)
    finally:
        db.close()

def login_user(request: HttpRequest, user: User):
    request.session['user_id'] = user.id

def logout_user(request: HttpRequest):
    request.session.flush()

def create_user(email: str, raw_password: str, is_admin: bool = False):
    db = SessionLocal()
    try:
        # Ensure unique email
        existing = db.query(User).filter(User.email == email).first()
        if existing:
            raise ValueError("Email already registered")
        user = User(email=email, password=make_password(raw_password), is_admin=is_admin)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    finally:
        db.close()

def verify_credentials(email: str, raw_password: str):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == email).first()
        if user and check_password(raw_password, user.password):
            return user
        return None
    finally:
        db.close()

def add_message(request: HttpRequest, level, text: str):
    messages.add_message(request, level, text)
