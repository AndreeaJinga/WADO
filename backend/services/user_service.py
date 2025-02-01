import bcrypt
import jwt
import json
from repositories.user_repository import UserRepository
from flask import current_app
from datetime import datetime, timedelta


class UserService:
    def __init__(self, db_path):
        self.user_repo = UserRepository(db_path)


    def register(self, username, plain_password):
        hashed_pw = bcrypt.hashpw(plain_password.encode('utf-8'), bcrypt.gensalt())
        hashed_pw_str = hashed_pw.decode('utf-8')
        user = self.user_repo.create_user(username, hashed_pw_str)
        return user


    def login(self, username, plain_password):
        user = self.user_repo.get_user_by_username(username)
        if not user:
            return None
        
        db_hashed_pw = user.password.encode('utf-8')
        if bcrypt.checkpw(plain_password.encode('utf-8'), db_hashed_pw):
            token = self._generate_jwt(username)
            return token
        else:
            return None

    def _generate_jwt(self, username):
        secret = current_app.config['JWT_SECRET_KEY']
        
        payload = {
            "username": username,
            "exp": datetime.utcnow() + timedelta(minutes=30)
        }
        
        token = jwt.encode(payload, secret, algorithm='HS256')
        return token
    
    
    def validate_token(self, token):
        secret = current_app.config['JWT_SECRET_KEY']
        try:
            decoded = jwt.decode(token, secret, algorithms=['HS256'])
            return decoded.get('username')
        except jwt.ExpiredSignatureError:
            print("Token has expired")
            return None
        except jwt.InvalidTokenError as e:
            print(e)
            print("Invalid token")
            return None
        

    def get_user_by_username(self, username):
        return self.user_repo.get_user_by_username(username)