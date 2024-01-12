from flask import Blueprint, request, jsonify
from app import db
from app.models.models import Tag
from app.common.decorators import token_required, role_required
from flasgger import swag_from
from datetime import datetime

tag_bp = Blueprint('tag', __name__)


@tag_bp.route('/tags', methods=['POST'])
@token_required
@role_required('admin')
@swag_from({
    'tags': ['Tag'],
    'description': 'Create a new tag.',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'name': {
                        'type': 'string',
                        'description': 'The name of the tag to be created.',
                    },
                },
                'required': ['name']
            }
        }
    ],
    'responses': {
        '201': {
            'description': 'Tag created successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'tag_id': {
                        'type': 'integer',
                        'description': 'The ID of the newly created tag',
                    },
                    'name': {
                        'type': 'string',
                        'description': 'The name of the tag',
                    },
                    'user_id': {
                        'type': 'integer',
                        'description': 'The ID of the user who created the tag',
                    },
                    'created_at': {
                        'type': 'string',
                        'format': 'date-time',
                        'description': 'The timestamp when the tag was created',
                    }
                }
            },
            'examples': {
                'application/json': {
                    'tag_id': 1,
                    'name': 'Machine Learning',
                    'user_id': 2,
                    'created_at': '2023-11-06T14:20:30Z'
                }
            }
        },
        '400': {
            'description': 'Bad request, possibly due to missing name or invalid data',
            'examples': {
                'application/json': {
                    'message': 'Name is required.'
                }
            }
        },
        '401': {
            'description': 'Unauthorized, token is missing or invalid'
        },
        '403': {
            'description': 'Forbidden, admin access required'
        }
    }
})
def create_tag(current_user):
    data = request.get_json()
    name = data.get('name')
    if not name:
        return jsonify({'message': 'Name is required.'}), 400

    new_tag = Tag(name=name, user_id=current_user.user_id)
    db.session.add(new_tag)
    db.session.commit()

    return jsonify({
        'tag_id': new_tag.tag_id,
        'name': new_tag.name,
        'user_id': new_tag.user_id,
        'created_at': new_tag.created_at
    }), 201


@tag_bp.route('/tags/<int:tag_id>', methods=['GET'])
@token_required
@role_required('staff')
@swag_from({
    'tags': ['Tag'],
    'description': 'Retrieve a specific tag by its ID.',
    'parameters': [
        {
            'name': 'tag_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'The unique ID of the tag to retrieve.',
        }
    ],
    'responses': {
        '200': {
            'description': 'Tag found and returned successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'tag_id': {
                        'type': 'integer',
                        'description': 'The ID of the tag',
                    },
                    'name': {
                        'type': 'string',
                        'description': 'The name of the tag',
                    },
                    'user_id': {
                        'type': 'integer',
                        'description': 'The ID of the user who created the tag',
                    },
                    'created_at': {
                        'type': 'string',
                        'format': 'date-time',
                        'description': 'The timestamp when the tag was created',
                    }
                }
            },
            'examples': {
                'application/json': {
                    'tag_id': 1,
                    'name': 'Machine Learning',
                    'user_id': 2,
                    'created_at': '2023-11-06T14:20:30Z'
                }
            }
        },
        '404': {
            'description': 'Tag not found for the given ID',
            'examples': {
                'application/json': {
                    'message': 'Tag not found.'
                }
            }
        },
        '401': {
            'description': 'Unauthorized, token is missing or invalid'
        },
        '403': {
            'description': 'Forbidden, staff access required'
        }
    }
})
def get_tag(current_user, tag_id: int):
    tag = Tag.query.get(tag_id)
    if not tag:
        return jsonify({'message': 'Tag not found.'}), 404

    return jsonify({
        'tag_id': tag.tag_id,
        'name': tag.name,
        'user_id': tag.user_id,
        'created_at': tag.created_at
    }), 200


@tag_bp.route('/tags/<int:tag_id>', methods=['PUT'])
@token_required
@role_required('admin')
@swag_from({
    'tags': ['Tag'],
    'description': 'Update the details of an existing tag.',
    'parameters': [
        {
            'name': 'tag_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'The unique ID of the tag to update.',
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'id': 'TagUpdate',
                'required': ['name'],
                'properties': {
                    'name': {
                        'type': 'string',
                        'description': 'The new name of the tag.',
                    },
                },
            },
        }
    ],
    'responses': {
        '200': {
            'description': 'Tag updated successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'tag_id': {
                        'type': 'integer',
                        'description': 'The ID of the tag',
                    },
                    'name': {
                        'type': 'string',
                        'description': 'The updated name of the tag',
                    },
                    'user_id': {
                        'type': 'integer',
                        'description': 'The ID of the user who created the tag',
                    },
                    'created_at': {
                        'type': 'string',
                        'format': 'date-time',
                        'description': 'The timestamp when the tag was created',
                    }
                }
            },
            'examples': {
                'application/json': {
                    'tag_id': 1,
                    'name': 'Data Science',
                    'user_id': 2,
                    'created_at': '2023-11-06T14:20:30Z'
                }
            }
        },
        '404': {
            'description': 'Tag not found for the given ID',
            'examples': {
                'application/json': {
                    'message': 'Tag not found.'
                }
            }
        },
        '401': {
            'description': 'Unauthorized, token is missing or invalid'
        },
        '403': {
            'description': 'Forbidden, admin access required or unauthorized action'
        }
    }
})
def update_tag(current_user, tag_id: int):
    tag = Tag.query.get(tag_id)
    if not tag:
        return jsonify({'message': 'Tag not found.'}), 404

    if tag.user_id != current_user.user_id:
        return jsonify({'message': 'Unauthorized.'}), 403

    data = request.get_json()
    tag.name = data.get('name', tag.name)
    db.session.commit()

    return jsonify({
        'tag_id': tag.tag_id,
        'name': tag.name,
        'user_id': tag.user_id,
        'created_at': tag.created_at
    }), 200


@tag_bp.route('/tags/<int:tag_id>', methods=['DELETE'])
@token_required
@role_required('admin')
@swag_from({
    'tags': ['Tag'],
    'description': 'Delete a tag by its ID.',
    'parameters': [
        {
            'name': 'tag_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'The unique ID of the tag to be deleted.',
        }
    ],
    'responses': {
        '200': {
            'description': 'Tag deleted successfully',
            'examples': {
                'application/json': {
                    'message': 'Tag deleted.'
                }
            }
        },
        '404': {
            'description': 'Tag not found for the given ID',
            'examples': {
                'application/json': {
                    'message': 'Tag not found.'
                }
            }
        },
        '401': {
            'description': 'Unauthorized, token is missing or invalid'
        },
        '403': {
            'description': 'Forbidden, admin access required or unauthorized action',
            'examples': {
                'application/json': {
                    'message': 'Unauthorized.'
                }
            }
        }
    }
})
def delete_tag(current_user, tag_id: int):
    tag = Tag.query.get(tag_id)
    if not tag:
        return jsonify({'message': 'Tag not found.'}), 404

    if tag.user_id != current_user.user_id:
        return jsonify({'message': 'Unauthorized.'}), 403

    db.session.delete(tag)
    db.session.commit()

    return jsonify({'message': 'Tag deleted.'}), 200


@tag_bp.route('/tags', methods=['GET'])
@token_required
@role_required('staff')
@swag_from({
    'tags': ['Tag'],
    'description': 'Retrieve a list of tags, with optional search filters.',
    'parameters': [
        {
            'name': 'name',
            'in': 'query',
            'type': 'string',
            'description': 'Filter tags by name, case insensitive, partial match',
        },
        {
            'name': 'user_id',
            'in': 'query',
            'type': 'integer',
            'description': 'Filter tags by the ID of the user who created them',
        },
        {
            'name': 'created_before',
            'in': 'query',
            'type': 'string',
            'format': 'date-time',
            'description': 'Filter tags created before a specific timestamp (YYYY-MM-DDTHH:MM:SS format)',
        },
        {
            'name': 'created_after',
            'in': 'query',
            'type': 'string',
            'format': 'date-time',
            'description': 'Filter tags created after a specific timestamp (YYYY-MM-DDTHH:MM:SS format)',
        }
    ],
    'responses': {
        '200': {
            'description': 'A list of tags',
            'schema': {
                'type': 'object',
                'properties': {
                    'tags': {
                        'type': 'array',
                        'items': {
                            '$ref': '#/definitions/Tag'
                        }
                    }
                }
            },
            'examples': {
                'application/json': {
                    'tags': [
                        {
                            'tag_id': 1,
                            'name': 'Python',
                            'user_id': 42,
                            'created_at': '2023-11-06T12:00:00'
                        },
                        {
                            'tag_id': 2,
                            'name': 'Flask',
                            'user_id': 42,
                            'created_at': '2023-11-06T13:00:00'
                        }
                    ]
                }
            }
        },
        '400': {
            'description': 'Bad request due to invalid parameters'
        }
    }
})
def list_tags(current_user):
    query = Tag.query
    name = request.args.get('name')
    user_id = request.args.get('user_id')
    created_before = request.args.get('created_before')
    created_after = request.args.get('created_after')

    if name:
        query = query.filter(Tag.name.ilike(f'%{name}%'))
    if user_id:
        query = query.filter_by(user_id=user_id)
    if created_before:
        try:
            created_before_date = datetime.strptime(
                created_before, '%Y-%m-%dT%H:%M:%S')
            query = query.filter(Tag.created_at <= created_before_date)
        except ValueError:
            return jsonify({'message': 'Invalid created_before datetime format. Use YYYY-MM-DDTHH:MM:SS.'}), 400
    if created_after:
        try:
            created_after_date = datetime.strptime(
                created_after, '%Y-%m-%dT%H:%M:%S')
            query = query.filter(Tag.created_at >= created_after_date)
        except ValueError:
            return jsonify({'message': 'Invalid created_after datetime format. Use YYYY-MM-DDTHH:MM:SS.'}), 400

    tags = query.all()

    return jsonify(tags=[{
        'tag_id': tag.tag_id,
        'name': tag.name,
        'user_id': tag.user_id,
        'created_at': tag.created_at.isoformat()
    } for tag in tags]), 200
