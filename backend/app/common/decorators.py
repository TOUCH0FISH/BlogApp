from functools import wraps
from flask import request, jsonify
from app.services.services import decode_token
from app.models.models import User


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(' ')[1]

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = decode_token(token)
            current_user = User.query.filter_by(
                user_id=data['user_id']).first()
            if current_user is None:
                raise RuntimeError('User not found.')
        except Exception as e:
            return jsonify({'message': str(e)}), 401

        return f(current_user, *args, **kwargs)
    




    return decorated


def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(current_user, *args, **kwargs):
            if current_user.role != role:
                return jsonify({'message': f'{role.capitalize()} access required'}), 403
            return f(current_user, *args, **kwargs)
        return decorated_function
    return decorator
