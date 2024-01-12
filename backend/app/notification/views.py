from flask import Blueprint, request, jsonify
from app import db
from app.models.models import Notification
from flasgger import swag_from
from app.common.decorators import token_required, role_required

notification_bp = Blueprint(
    'notification_bp', __name__, url_prefix='/notifications')


@notification_bp.route('', methods=['POST'])
@token_required
@role_required('admin')
@swag_from({
    'tags': ['Notification'],
    'description': 'Create a new notification',
    'parameters': [
        {
            'name': 'message',
            'in': 'formData',
            'type': 'string',
            'required': True,
            'description': 'Message content of the notification'
        },
        {
            'name': 'user_id',
            'in': 'formData',
            'type': 'integer',
            'required': True,
            'description': 'User ID to associate with the notification'
        }
    ],
    'responses': {
        '201': {
            'description': 'Notification created successfully',
            'examples': {
                'application/json': {
                    'notification_id': 1
                }
            }
        },
        '400': {
            'description': 'Invalid input or missing data',
        },
        '401': {
            'description': 'Unauthorized access',
        }
    }
})
def create_notification(current_user):
    data = request.get_json()
    message = data.get('message')
    user_id = data.get('user_id')
    if not message:
        return jsonify({'message': 'Message is required'}), 400
    
    if not user_id:
        return jsonify({'message': 'User ID is required'}), 400

    new_notification = Notification(message=message, user_id=user_id)
    db.session.add(new_notification)
    db.session.commit()

    return jsonify({'notification_id': new_notification.notification_id}), 201


@notification_bp.route('/<int:notification_id>', methods=['PUT'])
@token_required
@role_required('admin')
@swag_from({
    'tags': ['Notification'],
    'description': 'Update an existing notification',
    'parameters': [
        {
            'name': 'notification_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'Unique ID of the notification to be updated'
        }
    ],
    'requestBody': {
        'description': 'JSON object containing the updated data',
        'required': True,
        'content': {
            'application/json': {
                'schema': {
                    'type': 'object',
                    'properties': {
                        'message': {
                            'type': 'string',
                            'description': 'Updated notification message'
                        },
                        'user_id': {
                            'type': 'integer',
                            'description': 'Updated user ID associated with the notification'
                        }
                    },
                    'example': {
                        'message': 'Updated notification message',
                        'user_id': 2
                    }
                }
            }
        }
    },
    'responses': {
        '200': {
            'description': 'Notification successfully updated',
            'examples': {
                'application/json': {
                    'message': 'Notification updated'
                }
            }
        },
        '404': {
            'description': 'Notification not found',
        },
        '400': {
            'description': 'Invalid request data',
        },
        '401': {
            'description': 'Unauthorized access',
        }
    }
})
def update_notification(current_user, notification_id: int):
    notification = Notification.query.get(notification_id)
    if not notification:
        return jsonify({'message': 'Notification not found'}), 404

    data = request.get_json()
    notification.message = data.get('message', notification.message)
    notification.user_id = data.get('user_id', notification.user_id)

    db.session.commit()

    return jsonify({'message': 'Notification updated'}), 200


@notification_bp.route('/<int:notification_id>', methods=['GET'])
@token_required
@swag_from({
    'tags': ['Notification'],
    'description': 'Get a specific notification',
    'parameters': [
        {
            'name': 'notification_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'Unique ID of the notification'
        }
    ],
    'responses': {
        '200': {
            'description': 'Notification details',
            'examples': {
                'application/json': {
                    'notification_id': 1,
                    'message': 'Notification message',
                    'user_id': 1,
                    'created_at': '2023-01-01T00:00:00'
                }
            }
        },
        '404': {
            'description': 'Notification not found',
        },
        '401': {
            'description': 'Unauthorized access',
        }
    }
})
def get_notification(current_user, notification_id: int):
    notification = Notification.query.get(notification_id)
    if not notification:
        return jsonify({'message': 'Notification not found'}), 404

    return jsonify(notification.serialize()), 200


@notification_bp.route('/<int:notification_id>', methods=['DELETE'])
@token_required
@role_required('admin')
@swag_from({
    'tags': ['Notification'],
    'description': 'Delete a specific notification',
    'parameters': [
        {
            'name': 'notification_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'Unique ID of the notification to delete'
        }
    ],
    'responses': {
        '200': {
            'description': 'Notification successfully deleted',
            'examples': {
                'application/json': {
                    'message': 'Notification deleted'
                }
            }
        },
        '404': {
            'description': 'Notification not found',
        },
        '401': {
            'description': 'Unauthorized access',
        }
    }
})
def delete_notification(current_user, notification_id: int):
    notification = Notification.query.get(notification_id)
    if not notification:
        return jsonify({'message': 'Notification not found'}), 404

    db.session.delete(notification)
    db.session.commit()

    return jsonify({'message': 'Notification deleted'}), 200


@notification_bp.route('', methods=['GET'])
@token_required
@role_required('admin')
@swag_from({
    'tags': ['Notification'],
    'description': 'Retrieve a list of all notifications, with optional filtering parameters',
    'parameters': [
        {
            'name': 'message',
            'in': 'query',
            'type': 'string',
            'required': False,
            'description': 'Filter notifications by message content'
        },
        {
            'name': 'created_before',
            'in': 'query',
            'type': 'string',
            'format': 'date-time',
            'required': False,
            'description': 'Filter notifications created before a specific date and time'
        },
        {
            'name': 'created_after',
            'in': 'query',
            'type': 'string',
            'format': 'date-time',
            'required': False,
            'description': 'Filter notifications created after a specific date and time'
        }
    ],
    'responses': {
        '200': {
            'description': 'List of notifications',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'array',
                        'items': {
                            '$ref': '#/components/schemas/Notification'
                        }
                    },
                    'examples': {
                        'application/json': {
                            'value': [
                                {
                                    'notification_id': 1,
                                    'message': 'Notification message',
                                    'user_id': 2,
                                    'created_at': '2023-11-11T12:00:00Z'
                                },
                                {
                                    'notification_id': 2,
                                    'message': 'Another notification message',
                                    'user_id': 3,
                                    'created_at': '2023-11-10T11:00:00Z'
                                }
                            ]
                        }
                    }
                }
            }
        },
        '401': {
            'description': 'Unauthorized access',
        }
    }
})
def get_notifications(current_user):
    query = Notification.query
    message = request.args.get('message')
    created_before = request.args.get('created_before')
    created_after = request.args.get('created_after')

    if message:
        query = query.filter(Notification.message.contains(message))
    if created_before:
        query = query.filter(Notification.created_at <= created_before)
    if created_after:
        query = query.filter(Notification.created_at >= created_after)

    notifications = query.all()
    return jsonify([notification.serialize() for notification in notifications]), 200
