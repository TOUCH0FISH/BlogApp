from flask import Blueprint, request, jsonify
from app import db
from app.models.models import User
from app.services.services import register_user
from flasgger import swag_from
from app.common.decorators import token_required, role_required

user_bp = Blueprint('user', __name__)


@user_bp.route('/users', methods=['POST'])
@token_required
@role_required('admin')
@swag_from({
    'tags': ['User'],
    'description': 'Create a new user',
    'parameters': [
        {
            'name': 'username',
            'description': 'Username of the new user',
            'in': 'body',
            'type': 'string',
            'required': True
        },
        {
            'name': 'password',
            'description': 'Password for the new user',
            'in': 'body',
            'type': 'string',
            'required': True
        },
        {
            'name': 'role',
            'description': 'Role of the new user',
            'in': 'body',
            'type': 'string',
            'required': True
        }
    ],
    'responses': {
        '201': {
            'description': 'User created successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'user': {
                        'type': 'object',
                        'properties': {
                            # ... describe the user object properties
                        }
                    }
                }
            }
        },
        '400': {
            'description': 'Required fields are missing',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {
                        'type': 'string',
                        'example': 'Required fields are missing'
                    }
                }
            }
        }
    }
})
def create_user(current_user):
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    role = data.get('role')

    if username and password and role:
        user = register_user(username, password, role)
        if user:
            return jsonify(user=user.serialize()), 201
        return jsonify(message='Required fields are missing'), 400


@user_bp.route('/users/<int:user_id>', methods=['GET'])
@token_required
@role_required('admin')
@swag_from({
    'tags': ['User'],
    'description': 'Get a specific user',
    'parameters': [
        {
            'name': 'user_id',
            'description': 'ID of the user to be fetched',
            'in': 'path',
            'type': 'integer',
            'required': True
        }
    ],
    'responses': {
        '200': {
            'description': 'User fetched successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'user': {
                        'type': 'object',
                        'properties': {
                            # ... describe the user object properties
                        }
                    }
                }
            }
        },
        '404': {
            'description': 'User not found',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {
                        'type': 'string',
                        'example': 'User not found'
                    }
                }
            }
        }
    }
})
def get_user(current_user, user_id: int):
    user = User.query.get(user_id)
    if user:
        return jsonify(user=user.serialize()), 200
    return jsonify(message='User not found'), 404


@user_bp.route('/users/<int:user_id>', methods=['PUT'])
@token_required
@role_required('admin')
@swag_from({
    'tags': ['User'],
    'description': 'Update an existing user',
    'parameters': [
        {
            'name': 'user_id',
            'description': 'ID of the user to be updated',
            'in': 'path',
            'type': 'integer',
            'required': True
        },
        {
            'name': 'username',
            'description': 'New username for the user',
            'in': 'body',
            'type': 'string',
            'required': False
        },
        {
            'name': 'role',
            'description': 'New role for the user',
            'in': 'body',
            'type': 'string',
            'required': False
        }
    ],
    'responses': {
        '200': {
            'description': 'User updated successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'user': {
                        'type': 'object',
                        'properties': {
                            # ... describe the user object properties
                        }
                    }
                }
            }
        },
        '404': {
            'description': 'User not found',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {
                        'type': 'string',
                        'example': 'User not found'
                    }
                }
            }
        }
    }
})
def update_user(current_user, user_id: int):
    data = request.get_json()
    user = User.query.get(user_id)
    if user:
        user.username = data.get('username', user.username)
        user.role = data.get('role', user.role)
        db.session.commit()
        return jsonify(user=user.serialize()), 200
    return jsonify(message='User not found'), 404


@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
@token_required
@role_required('admin')
@swag_from({
    'tags': ['User'],
    'description': 'Delete a specific user',
    'parameters': [
        {
            'name': 'user_id',
            'description': 'ID of the user to be deleted',
            'in': 'path',
            'type': 'integer',
            'required': True
        }
    ],
    'responses': {
        '200': {
            'description': 'User deleted successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {
                        'type': 'string',
                        'example': 'User deleted'
                    }
                }
            }
        },
        '404': {
            'description': 'User not found',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {
                        'type': 'string',
                        'example': 'User not found'
                    }
                }
            }
        }
    }
})
def delete_user(current_user, user_id: int):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify(message='User deleted'), 200
    return jsonify(message='User not found'), 404


@user_bp.route('/users', methods=['GET'])
@token_required
@role_required('admin')
@swag_from({
    'tags': ['User'],
    'description': 'List all users',
    'responses': {
        '200': {
            'description': 'List of users',
            'schema': {
                'type': 'object',
                'properties': {
                    'users': {
                        'type': 'array',
                        'items': {
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
                                },
                            }
                        }
                    }
                }
            }
        }
    }
})
def list_users(current_user):
    users = User.query.all()
    return jsonify(users=[user.serialize() for user in users]), 200
