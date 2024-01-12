from flask import Blueprint, request, jsonify
from app import db
from app.models.models import Program
from flasgger import swag_from
from app.common.decorators import token_required, role_required

program_bp = Blueprint('program', __name__, url_prefix='/programs')


@program_bp.route('', methods=['POST'])
@token_required
@role_required('admin')
@swag_from({
    'tags': ['Program'],
    'description': 'Create a new program',
    'parameters': [
        {
            'name': 'name',
            'in': 'body',
            'type': 'string',
            'required': True,
            'description': 'The name of the program',
        },
        {
            'name': 'description',
            'in': 'body',
            'type': 'string',
            'required': False,
            'description': 'A brief description of the program',
        },
        {
            'name': 'version',
            'in': 'body',
            'type': 'string',
            'required': False,
            'description': 'The version of the program',
        }
    ],
    'responses': {
        201: {
            'description': 'Program created successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'program_id': {
                        'type': 'integer',
                        'description': 'The ID of the program'
                    },
                    'name': {
                        'type': 'string',
                        'description': 'The name of the program'
                    },
                    'description': {
                        'type': 'string',
                        'description': 'The description of the program'
                    },
                    'version': {
                        'type': 'string',
                        'description': 'The version of the program'
                    }
                }
            }
        },
        400: {
            'description': 'Name is required',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {
                        'type': 'string'
                    }
                }
            }
        }
    }
})
def create_program(current_user):
    data = request.get_json()
    name = data.get('name')
    description = data.get('description', '')
    version = data.get('version', '')

    if name:
        new_program = Program(
            name=name, description=description, version=version)
        db.session.add(new_program)
        db.session.commit()
        return jsonify(program_id=new_program.program_id, name=new_program.name,
                       description=new_program.description, version=new_program.version), 201
    else:
        return jsonify(message='Name is required.'), 400


@program_bp.route('/<int:program_id>', methods=['GET'])
@token_required
@role_required('staff')
@swag_from({
    'tags': ['Program'],
    'description': 'Get a specific program by its ID',
    'parameters': [
        {
            'name': 'program_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'The ID of the program to retrieve',
        }
    ],
    'responses': {
        200: {
            'description': 'Program retrieved successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'program_id': {
                        'type': 'integer',
                        'description': 'The ID of the program'
                    },
                    'name': {
                        'type': 'string',
                        'description': 'The name of the program'
                    },
                    'description': {
                        'type': 'string',
                        'description': 'The description of the program'
                    },
                    'version': {
                        'type': 'string',
                        'description': 'The version of the program'
                    }
                }
            }
        },
        404: {
            'description': 'Program not found',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {
                        'type': 'string'
                    }
                }
            }
        }
    }
})
def get_program(current_user, program_id: int):
    program = Program.query.get(program_id)
    if program:
        return jsonify(program_id=program.program_id, name=program.name,
                       description=program.description, version=program.version), 200
    return jsonify(message='Program not found'), 404


@program_bp.route('/<int:program_id>', methods=['PUT'])
@token_required
@role_required('admin')
@swag_from({
    'tags': ['Program'],
    'description': 'Update an existing program by its ID',
    'parameters': [
        {
            'name': 'program_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'The ID of the program to update',
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
                        'description': 'The updated name of the program',
                    },
                    'description': {
                        'type': 'string',
                        'description': 'The updated description of the program',
                    },
                    'version': {
                        'type': 'string',
                        'description': 'The updated version of the program',
                    }
                }
            },
            'description': 'The updated information of the program',
        }
    ],
    'responses': {
        200: {
            'description': 'Program updated successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'program_id': {
                        'type': 'integer',
                        'description': 'The ID of the updated program'
                    },
                    'name': {
                        'type': 'string',
                        'description': 'The updated name of the program'
                    },
                    'description': {
                        'type': 'string',
                        'description': 'The updated description of the program'
                    },
                    'version': {
                        'type': 'string',
                        'description': 'The updated version of the program'
                    }
                }
            }
        },
        404: {
            'description': 'Program not found',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {
                        'type': 'string'
                    }
                }
            }
        }
    }
})
def update_program(current_user, program_id: int):
    data = request.get_json()
    program = Program.query.get(program_id)

    if program:
        program.name = data.get('name', program.name)
        program.description = data.get('description', program.description)
        program.version = data.get('version', program.version)
        db.session.commit()
        return jsonify(program_id=program.program_id, name=program.name,
                       description=program.description, version=program.version), 200
    else:
        return jsonify(message='Program not found.'), 404


@program_bp.route('/<int:program_id>', methods=['DELETE'])
@token_required
@role_required('admin')
@swag_from({
    'tags': ['Program'],
    'description': 'Delete a program by its ID',
    'parameters': [
        {
            'name': 'program_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'The ID of the program to delete',
        }
    ],
    'responses': {
        200: {
            'description': 'Program deleted successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {
                        'type': 'string'
                    }
                }
            }
        },
        404: {
            'description': 'Program not found',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {
                        'type': 'string'
                    }
                }
            }
        }
    }
})
def delete_program(current_user, program_id: int):
    program = Program.query.get(program_id)

    if program:
        db.session.delete(program)
        db.session.commit()
        return jsonify(message='Program deleted.'), 200
    else:
        return jsonify(message='Program not found.'), 404


@program_bp.route('', methods=['GET'])
@token_required
@role_required('admin')
@swag_from({
    'tags': ['Program'],
    'description': 'List/search all programs with optional query parameters for filtering by name and/or version',
    'parameters': [
        {
            'name': 'name',
            'in': 'query',
            'type': 'string',
            'required': False,
            'description': 'Filter programs by name, case insensitive, partial match'
        },
        {
            'name': 'version',
            'in': 'query',
            'type': 'string',
            'required': False,
            'description': 'Filter programs by version'
        }
    ],
    'responses': {
        200: {
            'description': 'A list of filtered programs, if any filters are provided; otherwise all programs',
            'schema': {
                'type': 'object',
                'properties': {
                    'programs': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'program_id': {
                                    'type': 'integer',
                                    'description': 'The unique identifier of the program'
                                },
                                'name': {
                                    'type': 'string',
                                    'description': 'The name of the program'
                                },
                                'description': {
                                    'type': 'string',
                                    'description': 'A description of the program'
                                },
                                'version': {
                                    'type': 'string',
                                    'description': 'The version of the program'
                                }
                            }
                        }
                    }
                }
            }
        }
    }
})
def list_programs(current_user):
    name = request.args.get('name')
    version = request.args.get('version')
    query = Program.query

    if name:
        query = query.filter(Program.name.ilike(f'%{name}%'))
    if version:
        query = query.filter(Program.version.ilike(f'%{version}%'))

    programs = query.all()
    programs_data = [{
        'program_id': program.program_id,
        'name': program.name,
        'description': program.description,
        'version': program.version
    } for program in programs]

    return jsonify(programs=programs_data), 200
