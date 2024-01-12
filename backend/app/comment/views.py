from flask import Blueprint, request, jsonify
from app import db
from app.models.models import Comment, Material, Module, Tag
from flasgger import swag_from
from app.common.decorators import token_required
from app.tasks import send_notification

comment_bp = Blueprint('comment_bp', __name__, url_prefix='/comments')


@comment_bp.route('', methods=['POST'])
@token_required
@swag_from({
    'tags': ['Comment'],
    'parameters': [
        {'name': 'body', 'in': 'body', 'required': True, 'schema': {
            'type': 'object',
            'properties': {
                'text': {'type': 'string'},
                'material_id': {'type': 'integer'}
            },
            'required': ['text', 'material_id']
        }},
    ],
    'responses': {
        '201': {
            'description': 'Comment created successfully',
            'examples': {
                'application/json': {
                    'comment_id': 1
                }
            }
        },
        '404': {
            'description': 'Material not found'
        }
    }
})
def create_comment(current_user):
    data = request.get_json()
    text = data.get('text')
    material_id = data.get('material_id')

    # Validate material_id
    material = Material.query.get(material_id)
    if not material:
        return jsonify({'message': 'Material not found.'}), 404

    new_comment = Comment(
        text=text, user_id=current_user.user_id, material_id=material_id)
    db.session.add(new_comment)
    db.session.commit()

    # Trigger the Celery task
    send_notification.delay(
        material.user_id, f'New comment created: \n{Module.query.get(material.module_id).name}\n{Tag.query.get(material.tag_id).name}\n{material.title}')

    return jsonify({'comment_id': new_comment.comment_id}), 201


@comment_bp.route('/<int:comment_id>', methods=['GET'])
@token_required
@swag_from({
    'tags': ['Comment'],
    'parameters': [
        {'name': 'comment_id', 'in': 'path', 'required': True,
            'type': 'integer', 'description': 'The ID of the comment'}
    ],
    'responses': {
        '200': {
            'description': 'Details of a specific comment',
            'examples': {
                'application/json': {
                    'comment_id': 1,
                    'text': 'Great material!',
                    'created_at': '2023-11-06T12:00:00',
                    'user_id': 2,
                    'material_id': 5
                }
            }
        },
        '404': {
            'description': 'Comment not found'
        }
    }
})
def get_comment(current_user, comment_id: int):
    comment = Comment.query.get(comment_id)
    if not comment:
        return jsonify({'message': 'Comment not found.'}), 404

    return jsonify(comment.serialize()), 200


@comment_bp.route('/<int:comment_id>', methods=['PUT'])
@token_required
@swag_from({
    'tags': ['Comment'],
    'parameters': [
        {'name': 'comment_id', 'in': 'path', 'required': True,
            'type': 'integer', 'description': 'The ID of the comment to update'},
        {'name': 'body', 'in': 'body', 'required': True, 'schema': {
            'type': 'object',
            'properties': {
                'text': {'type': 'string'}
            },
            'required': ['text']
        }},
    ],
    'responses': {
        '200': {
            'description': 'Comment updated successfully'
        },
        '404': {
            'description': 'Comment not found'
        },
        '403': {
            'description': 'Unauthorized to update comment'
        }
    }
})
def update_comment(current_user, comment_id: int):
    comment = Comment.query.get(comment_id)
    if not comment:
        return jsonify({'message': 'Comment not found.'}), 404

    # Check if the current user is the owner of the comment
    if comment.user_id != current_user.user_id:
        return jsonify({'message': 'Unauthorized.'}), 403

    data = request.get_json()
    comment.text = data.get('text', comment.text)
    db.session.commit()

    return jsonify(comment.serialize()), 200


@comment_bp.route('/<int:comment_id>', methods=['DELETE'])
@token_required
@swag_from({
    'tags': ['Comment'],
    'parameters': [
        {'name': 'comment_id', 'in': 'path', 'required': True,
            'type': 'integer', 'description': 'The ID of the comment to delete'}
    ],
    'responses': {
        '200': {
            'description': 'Comment deleted successfully',
            'examples': {
                'application/json': {
                    'message': 'Comment deleted.'
                }
            }
        },
        '404': {
            'description': 'Comment not found'
        },
        '403': {
            'description': 'Unauthorized to delete comment'
        }
    }
})
def delete_comment(current_user, comment_id: int):
    comment = Comment.query.get(comment_id)
    if not comment:
        return jsonify({'message': 'Comment not found.'}), 404

    # Check if the current user is the owner of the comment
    if comment.user_id != current_user.user_id:
        return jsonify({'message': 'Unauthorized.'}), 403

    db.session.delete(comment)
    db.session.commit()

    return jsonify({'message': 'Comment deleted.'}), 200


@comment_bp.route('', methods=['GET'])
@token_required
@swag_from({
    'tags': ['Comment'],
    'parameters': [
        {'name': 'user_id', 'in': 'query', 'type': 'integer',
            'description': 'Filter by user ID'},
        {'name': 'material_id', 'in': 'query', 'type': 'integer',
            'description': 'Filter by material ID'},
        {'name': 'created_before', 'in': 'query', 'type': 'string',
            'description': 'Filter comments created before this date'},
        {'name': 'created_after', 'in': 'query', 'type': 'string',
            'description': 'Filter comments created after this date'}
    ],
    'responses': {
        '200': {
            'description': 'A list of comments',
            'examples': {
                'application/json': [
                    {
                        'comment_id': 1,
                        'text': 'Great material!',
                        'created_at': '2023-11-06T12:00:00',
                        'user_id': 2,
                        'material_id': 5
                    }
                ]
            }
        }
    }
})
def list_comments(current_user):
    user_id = request.args.get('user_id')
    material_id = request.args.get('material_id')
    created_before = request.args.get('created_before')
    created_after = request.args.get('created_after')

    query = Comment.query

    if user_id:
        query = query.filter_by(user_id=user_id)
    if material_id:
        query = query.filter_by(material_id=material_id)
    if created_before:
        query = query.filter(Comment.created_at < created_before)
    if created_after:
        query = query.filter(Comment.created_at > created_after)

    comments = query.all()

    return jsonify([comment.serialize() for comment in comments]), 200
