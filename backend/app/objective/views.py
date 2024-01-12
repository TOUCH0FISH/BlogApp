from flask import Blueprint, request, jsonify
from app import db
from app.models.models import Objective, Program
from flasgger import swag_from
from app.common.decorators import token_required, role_required

objective_bp = Blueprint('objective', __name__, url_prefix='/objectives')


@objective_bp.route('', methods=['POST'])
@token_required
@role_required('admin')
@swag_from({
    'tags': ['Objective'],
    'description': 'Create a new objective',
    'parameters': [
        {
            'name': 'name',
            'in': 'body',
            'type': 'string',
            'required': True,
            'description': 'Name of the objective',
        },
        {
            'name': 'description',
            'in': 'body',
            'type': 'string',
            'required': False,
            'description': 'Description of the objective',
        },
        {
            'name': 'program_id',
            'in': 'body',
            'type': 'integer',
            'required': True,
            'description': 'ID of the program associated with the objective',
        }
    ],
    'responses': {
        201: {
            'description': 'Objective created successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'objective_id': {
                        'type': 'integer',
                        'example': 1,
                    },
                    'name': {
                        'type': 'string',
                        'example': 'Objective Name',
                    },
                    'description': {
                        'type': 'string',
                        'example': 'Objective Description',
                    },
                    'program_id': {
                        'type': 'integer',
                        'example': 1,
                    }
                }
            }
        },
        400: {
            'description': 'Invalid input, object invalid'
        },
    }
})
def create_objective(current_user):
    data = request.get_json()
    name = data.get('name')
    description = data.get('description', '')
    program_id = data.get('program_id')

    # Validate program_id
    if program_id and not Program.query.get(program_id):
        return jsonify(message='Program ID is invalid or does not exist'), 400

    if name and program_id:
        new_objective = Objective(
            name=name, description=description, program_id=program_id)
        db.session.add(new_objective)
        db.session.commit()
        return jsonify({
            'objective_id': new_objective.objective_id,
            'name': new_objective.name,
            'description': new_objective.description,
            'program_id': new_objective.program_id
        }), 201
    else:
        return jsonify(message='Name and program ID are required'), 400


@objective_bp.route('/<int:objective_id>', methods=['PUT'])
@token_required
@role_required('admin')
@swag_from({
    'tags': ['Objective'],
    'description': 'Update an existing objective',
    'parameters': [
        {
            'name': 'objective_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'The ID of the objective to update',
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'name': {
                        'type': 'string',
                        'description': 'Updated name of the objective',
                        'example': 'Updated Objective Name'
                    },
                    'description': {
                        'type': 'string',
                        'description': 'Updated description of the objective',
                        'example': 'Updated Objective Description'
                    }
                },
                'required': ['name']
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Objective updated successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'objective_id': {
                        'type': 'integer',
                        'example': 1
                    },
                    'name': {
                        'type': 'string',
                        'example': 'Updated Objective Name'
                    },
                    'description': {
                        'type': 'string',
                        'example': 'Updated Objective Description'
                    },
                    'program_id': {
                        'type': 'integer',
                        'example': 1
                    }
                }
            }
        },
        404: {
            'description': 'Objective not found'
        }
    }
})
def update_objective(current_user, objective_id: int):
    objective = Objective.query.get(objective_id)
    if not objective:
        return jsonify(message='Objective not found'), 404
    data = request.get_json()
    program_id = data.get('program_id')

    # Validate program_id
    if program_id and not Program.query.get(program_id):
        return jsonify(message='Program ID is invalid or does not exist'), 400

    objective.name = data.get('name', objective.name)
    objective.description = data.get('description', objective.description)
    db.session.commit()
    return jsonify({
        'objective_id': objective.objective_id,
        'name': objective.name,
        'description': objective.description,
        'program_id': objective.program_id
    }), 200


@objective_bp.route('/<int:objective_id>', methods=['GET'])
@token_required
@role_required('staff')
@swag_from({
    'tags': ['Objective'],
    'description': 'Get a specific objective by ID',
    'parameters': [
        {
            'name': 'objective_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'Unique ID of the objective'
        }
    ],
    'responses': {
        200: {
            'description': 'Objective found',
            'schema': {
                'type': 'object',
                'properties': {
                    'objective_id': {
                        'type': 'integer',
                        'example': 1
                    },
                    'name': {
                        'type': 'string',
                        'example': 'Objective Name'
                    },
                    'description': {
                        'type': 'string',
                        'example': 'Objective Description'
                    },
                    'program_id': {
                        'type': 'integer',
                        'example': 1
                    }
                }
            }
        },
        404: {
            'description': 'Objective not found'
        }
    }
})
def get_objective(current_user, objective_id: int):
    objective = Objective.query.get(objective_id)
    if objective:
        return jsonify({
            'objective_id': objective.objective_id,
            'name': objective.name,
            'description': objective.description,
            'program_id': objective.program_id
        }), 200
    else:
        return jsonify(message='Objective not found'), 404


@objective_bp.route('/<int:objective_id>', methods=['DELETE'])
@token_required
@role_required('admin')
@swag_from({
    'tags': ['Objective'],
    'description': 'Delete a specific objective by ID',
    'parameters': [
        {
            'name': 'objective_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'Unique ID of the objective to delete'
        }
    ],
    'responses': {
        200: {
            'description': 'Objective deleted successfully',
            'examples': {
                'application/json': {
                    'message': 'Objective deleted'
                }
            }
        },
        404: {
            'description': 'Objective not found',
            'examples': {
                'application/json': {
                    'message': 'Objective not found'
                }
            }
        }
    }
})
def delete_objective(current_user, objective_id: int):
    objective = Objective.query.get(objective_id)
    if objective:
        db.session.delete(objective)
        db.session.commit()
        return jsonify(message='Objective deleted'), 200
    else:
        return jsonify(message='Objective not found'), 404


@objective_bp.route('', methods=['GET'])
@token_required
@role_required('staff')
@swag_from({
    'tags': ['Objective'],
    'description': 'List all objectives, with optional query parameters for filtering by program ID and/or name',
    'parameters': [
        {
            'name': 'program_id',
            'in': 'query',
            'type': 'integer',
            'required': False,
            'description': 'Filter objectives by program ID'
        },
        {
            'name': 'name',
            'in': 'query',
            'type': 'string',
            'required': False,
            'description': 'Filter objectives by name, case insensitive, partial match'
        }
    ],
    'responses': {
        200: {
            'description': 'A list of objectives',
            'schema': {
                'type': 'object',
                'properties': {
                    'objectives': {
                        'type': 'array',
                        'items': {
                            '$ref': '#/definitions/Objective'
                        }
                    }
                }
            },
            'examples': {
                'application/json': {
                    'objectives': [
                        {
                            'objective_id': 1,
                            'name': 'Objective Name',
                            'description': 'Objective Description',
                            'program_id': 1
                        }
                        # ... other objectives ...
                    ]
                }
            }
        }
    },
    'definitions': {
        'Objective': {
            'type': 'object',
            'properties': {
                'objective_id': {
                    'type': 'integer',
                    'example': 1
                },
                'name': {
                    'type': 'string',
                    'example': 'Objective Name'
                },
                'description': {
                    'type': 'string',
                    'example': 'Objective Description'
                },
                'program_id': {
                    'type': 'integer',
                    'example': 1
                }
            }
        }
    }
})
def list_objectives(current_user):
    program_id = request.args.get('program_id')
    name = request.args.get('name')
    query = Objective.query
    if program_id:
        query = query.filter(Objective.program_id == program_id)
    if name:
        query = query.filter(Objective.name.ilike(f'%{name}%'))
    objectives = query.all()
    objectives_data = [{
        'objective_id': obj.objective_id,
        'name': obj.name,
        'description': obj.description,
        'program_id': obj.program_id
    } for obj in objectives]
    return jsonify(objectives=objectives_data), 200
