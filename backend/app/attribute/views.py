from flask import Blueprint, request, jsonify
from app import db
from app.models.models import Attribute, Program
from flasgger import swag_from
from app.common.decorators import token_required, role_required

attribute_bp = Blueprint('attribute_bp', __name__,
                         url_prefix='/graduate-attributes')


@attribute_bp.route('', methods=['POST'])
@token_required
@role_required('admin')
@swag_from({
    'tags': ['Graduate Attribute'],
    'description': 'Create a new graduate attribute',
    'parameters': [
        {
            'name': 'name',
            'in': 'body',
            'type': 'string',
            'required': True,
            'description': 'Name of the graduate attribute',
        },
        {
            'name': 'description',
            'in': 'body',
            'type': 'string',
            'required': False,
            'description': 'Description of the graduate attribute',
        },
        {
            'name': 'program_id',
            'in': 'body',
            'type': 'integer',
            'required': True,
            'description': 'ID of the program the attribute belongs to',
        }
    ],
    'responses': {
        201: {
            'description': 'Attribute created successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'attribute_id': {
                        'type': 'integer',
                        'description': 'The ID of the created attribute',
                    },
                    'name': {
                        'type': 'string',
                        'description': 'The name of the created attribute',
                    },
                    'description': {
                        'type': 'string',
                        'description': 'The description of the created attribute',
                    },
                    'program_id': {
                        'type': 'integer',
                        'description': 'The program ID the attribute is associated with',
                    }
                }
            }
        },
        400: {
            'description': 'Invalid input, object invalid'
        },
    }
})
def create_attribute(current_user):
    data = request.get_json()
    name = data.get('name')
    description = data.get('description', '')
    program_id = data.get('program_id')

    if not all([name, program_id]):
        return jsonify(message='Name and program ID are required'), 400

    # Validate program_id
    if program_id and not Program.query.get(program_id):
        return jsonify(message='Program ID is invalid or does not exist'), 400

    new_attribute = Attribute(
        name=name, description=description, program_id=program_id)
    db.session.add(new_attribute)
    db.session.commit()

    return jsonify({
        'attribute_id': new_attribute.attribute_id,
        'name': new_attribute.name,
        'description': new_attribute.description,
        'program_id': new_attribute.program_id
    }), 201


@attribute_bp.route('/<int:attribute_id>', methods=['GET'])
@token_required
@role_required('staff')
@swag_from({
    'tags': ['Graduate Attribute'],
    'description': 'Get details of a specific graduate attribute',
    'parameters': [
        {
            'name': 'attribute_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'The ID of the graduate attribute to retrieve',
        }
    ],
    'responses': {
        200: {
            'description': 'Details of the graduate attribute',
            'schema': {
                'type': 'object',
                'properties': {
                    'attribute_id': {
                        'type': 'integer',
                        'description': 'The ID of the attribute',
                    },
                    'name': {
                        'type': 'string',
                        'description': 'The name of the attribute',
                    },
                    'description': {
                        'type': 'string',
                        'description': 'The description of the attribute',
                    },
                    'program_id': {
                        'type': 'integer',
                        'description': 'The program ID the attribute is associated with',
                    }
                }
            }
        },
        404: {
            'description': 'Attribute not found'
        },
    }
})
def get_attribute(current_user, attribute_id: int):
    attribute = Attribute.query.get(attribute_id)
    if attribute:
        return jsonify({
            'attribute_id': attribute.attribute_id,
            'name': attribute.name,
            'description': attribute.description,
            'program_id': attribute.program_id
        }), 200
    else:
        return jsonify(message='Attribute not found'), 404


@attribute_bp.route('/<int:attribute_id>', methods=['PUT'])
@token_required
@role_required('admin')
@swag_from({
    'tags': ['Graduate Attribute'],
    'description': 'Update an existing graduate attribute',
    'parameters': [
        {
            'name': 'attribute_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'The ID of the graduate attribute to update',
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'name': {'type': 'string', 'description': 'New name of the attribute'},
                    'description': {'type': 'string', 'description': 'New description of the attribute'},
                    'program_id': {'type': 'integer', 'description': 'New program ID associated with the attribute'}
                }
            },
            'description': 'JSON object with the new attribute details'
        }
    ],
    'responses': {
        200: {
            'description': 'Attribute successfully updated',
            'schema': {
                'type': 'object',
                'properties': {
                    'attribute_id': {
                        'type': 'integer',
                        'description': 'The ID of the updated attribute',
                    },
                    'name': {
                        'type': 'string',
                        'description': 'The new name of the attribute',
                    },
                    'description': {
                        'type': 'string',
                        'description': 'The new description of the attribute',
                    },
                    'program_id': {
                        'type': 'integer',
                        'description': 'The new program ID associated with the attribute',
                    }
                }
            }
        },
        404: {
            'description': 'Attribute not found'
        },
    }
})
def update_attribute(current_user, attribute_id: int):
    attribute = Attribute.query.get(attribute_id)
    data = request.get_json()
    program_id = data.get('program_id')

    # Validate program_id
    if program_id and not Program.query.get(program_id):
        return jsonify(message='Program ID is invalid or does not exist'), 400

    if not attribute:
        return jsonify(message='Attribute not found'), 404

    attribute.name = data.get('name', attribute.name)
    attribute.description = data.get('description', attribute.description)
    attribute.program_id = data.get('program_id', attribute.program_id)
    db.session.commit()

    return jsonify({
        'attribute_id': attribute.attribute_id,
        'name': attribute.name,
        'description': attribute.description,
        'program_id': attribute.program_id
    }), 200


@attribute_bp.route('/<int:attribute_id>', methods=['DELETE'])
@token_required
@role_required('admin')
@swag_from({
    'tags': ['Graduate Attribute'],
    'description': 'Delete a specific graduate attribute',
    'parameters': [
        {
            'name': 'attribute_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'The ID of the graduate attribute to delete',
        }
    ],
    'responses': {
        200: {
            'description': 'Attribute successfully deleted',
        },
        404: {
            'description': 'Attribute not found'
        },
    }
})
def delete_attribute(current_user, attribute_id: int):
    attribute = Attribute.query.get(attribute_id)
    if attribute:
        db.session.delete(attribute)
        db.session.commit()
        return jsonify(message='Attribute deleted'), 200
    else:
        return jsonify(message='Attribute not found'), 404


@attribute_bp.route('', methods=['GET'])
@token_required
@role_required('staff')
@swag_from({
    'tags': ['Graduate Attribute'],
    'description': 'List all graduate attributes, with optional query parameters for filtering by program ID and/or name',
    'parameters': [
        {
            'name': 'program_id',
            'in': 'query',
            'type': 'integer',
            'required': False,
            'description': 'Filter attributes by program ID'
        },
        {
            'name': 'name',
            'in': 'query',
            'type': 'string',
            'required': False,
            'description': 'Filter attributes by name, case insensitive, partial match'
        }
    ],
    'responses': {
        200: {
            'description': 'A list of all attributes',
            'schema': {
                'type': 'object',
                'properties': {
                    'attributes': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'attribute_id': {'type': 'integer'},
                                'name': {'type': 'string'},
                                'description': {'type': 'string'},
                                'program_id': {'type': 'integer'},
                            },
                        },
                    },
                },
            },
            'examples': {
                'application/json': {
                    'attributes': [
                        {
                            'attribute_id': 1,
                            'name': 'Critical Thinking',
                            'description': 'Ability to analyze issues critically',
                            'program_id': 1
                        }
                        # ... other attributes ...
                    ]
                }
            }
        }
    }
})
def list_attributes(current_user):
    program_id = request.args.get('program_id')
    name = request.args.get('name')
    query = Attribute.query

    if program_id:
        query = query.filter(Attribute.program_id == program_id)
    if name:
        query = query.filter(Attribute.name.ilike(f'%{name}%'))

    attributes = query.all()
    attributes_list = [{
        'attribute_id': attr.attribute_id,
        'name': attr.name,
        'description': attr.description,
        'program_id': attr.program_id
    } for attr in attributes]

    return jsonify(attributes=attributes_list), 200
