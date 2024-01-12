import bcrypt
import jwt
from datetime import datetime, timedelta
from flask import current_app
from app import db
from app.models.models import User

# Hashing

# # orign
# def hash_password(password: str) -> str:
#     # return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
#     return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
#     # hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def check_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

# JWT


def generate_token(user_id: int, role: str):
    expiration = datetime.utcnow(
    ) + timedelta(seconds=current_app.config['JWT_EXPIRATION'])
    return jwt.encode(
        {'user_id': user_id, 'role': role, 'exp': expiration},
        current_app.config['JWT_SECRET'],
        algorithm=current_app.config['JWT_ALGORITHM']
    )


def decode_token(token: str):
    return jwt.decode(token, current_app.config['JWT_SECRET'], algorithms=[current_app.config['JWT_ALGORITHM']])

# Authentication


def register_user(username: str, password: str, role: str) -> User:
    hashed_password = hash_password(password)
    new_user = User(username=username, password=hashed_password, role=role)
    db.session.add(new_user)
    db.session.commit()
    return new_user


def login_user(username: str, password: str):
    user = User.query.filter_by(username=username).first()
    if user and check_password(password, user.password):
        token = generate_token(user.user_id, user.role)
        return {'user': user, 'token': token}
    return None


def logout_user():
    return None


def update_password(username: str, password: str, new_password: str):
    user = User.query.filter_by(username=username).first()
    if user and check_password(password, user.password):
        user.password = hash_password(new_password)
        db.session.commit()
        return user
    return None
