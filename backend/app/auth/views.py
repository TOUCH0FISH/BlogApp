from flask import Blueprint, request, jsonify
from app.services.services import register_user, login_user, logout_user, update_password
from flasgger.utils import swag_from
from app.common.decorators import token_required

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/register', methods=['POST'])
@swag_from({
    'tags': ['Authentication'],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'id': 'UserRegistration',
                'required': ['username', 'password', 'role'],
                'properties': {
                    'username': {
                        'type': 'string',
                        'description': 'The username of the user being registered',
                    },
                    'password': {
                        'type': 'string',
                        'description': 'The password of the user being registered',
                    },
                    'role': {
                        'type': 'string',
                        'description': 'The role of the user being registered',
                    },
                },
            },
        },
    ],
    'responses': {
        '201': {
            'description': 'User registered successfully',
            'examples': {
                'application/json': {
                    'user': {
                        'user_id': 1,
                        'username': 'johndoe',
                        'role': 'user',
                    },
                },
            },
        },
        '400': {
            'description': 'Bad request, possibly due to missing parameters or registration failure',
            'examples': {
                'application/json': {
                    'message': 'Registration failed',
                },
                'application/json': {
                    'message': 'Username, password, and role are required',
                }
            },
        },
    },
})
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    role = data.get('role')

    if username and password and role:
        user = register_user(username, password, role)
        if user:
            return jsonify(user=user.serialize()), 201
        return jsonify(message='Registration failed'), 400

    return jsonify(message='Username, password, and role are required'), 400


@auth_bp.route('/login', methods=['POST'])
@swag_from({
    'tags': ['Authentication'],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': 'true',
            'schema': {
                'id': 'UserCredentials',
                'required': ['username', 'password'],
                'properties': {
                    'username': {
                        'type': 'string',
                        'description': 'The user name',
                    },
                    'password': {
                        'type': 'string',
                        'description': 'The user password',
                    },
                },
            },
        },
    ],
    'responses': {
        '200': {
            'description': 'Successfully logged in',
            'schema': {
                'type': 'object',
                'properties': {
                    'token': {
                        'type': 'string',
                        'example': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...',
                    },
                    'user': {
                        'type': 'object',
                        'properties': {
                            'user_id': {
                                'type': 'integer',
                                'example': 1
                            },
                            'username': {
                                'type': 'string',
                                'example': 'johndoe'
                            },
                            'role': {
                                'type': 'string',
                                'example': 'admin'
                            }
                        }
                    }
                }
            }
        },
        '401': {
            'description': 'Invalid credentials',
        },
    },
})
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if username and password:
        result = login_user(username, password)
        if result:
            token = result['token']
            user = result['user']
            return jsonify(token=token, user=user.serialize()), 200
        return jsonify(message='Authentication failed'), 401
    return jsonify(message='Username and password are required'), 400


@auth_bp.route('/logout', methods=['POST'])
@swag_from({
    'tags': ['Authentication'],
    'description': 'Logs out the current user',
    'responses': {
        '200': {
            'description': 'Logged out successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {
                        'type': 'string',
                        'example': 'Logged out'
                    }
                }
            }
        },
        '401': {
            'description': 'Unauthorized, token is missing or invalid'
        }
    }
})
def logout():
    # ...
    logout_user()
    return jsonify(message='Logged out'), 200


@auth_bp.route('/password', methods=['PUT'])
@token_required
@swag_from({
    'tags': ['Authentication'],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': 'true',
            'schema': {
                'id': 'UserPasswordUpdate',
                'required': ['username', 'password', 'new_password'],
                'properties': {
                    'username': {
                        'type': 'string',
                        'description': 'The user name',
                    },
                    'password': {
                        'type': 'string',
                        'description': 'The current password',
                    },
                    'new_password': {
                        'type': 'string',
                        'description': 'The new password',
                    },
                },
            },
        },
    ],
    'responses': {
        '200': {
            'description': 'Password updated successfully',
            'examples': {
                'application/json': {
                    'message': 'Password updated',
                }
            }
        },
        '400': {
            'description': 'Bad request, possibly due to missing parameters or wrong credentials',
            'examples': {
                'application/json': {
                    'message': 'Update failed',
                },
                'application/json': {
                    'message': 'Username, password, and new password are required',
                }
            }
        },
    },
})
def update_user_password(current_user):
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    new_password = data.get('new_password')

    # Ensure the current user is the one making the request
    if username != current_user.username:
        return jsonify(message='You can only update your own password.'), 403

    if username and password and new_password:
        user = update_password(username, password, new_password)
        if user:
            return jsonify(message='Password updated'), 200
        return jsonify(message='Update failed'), 400
    return jsonify(message='Username, password, and new password are required'), 400
