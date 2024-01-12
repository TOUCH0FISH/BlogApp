from flask import Blueprint, request, jsonify
from app import db
from app.models.models import Module, Program
from flasgger import swag_from
from app.common.decorators import token_required, role_required

module_bp = Blueprint('module_bp', __name__,
                      url_prefix='/modules')


@module_bp.route('', methods=['POST'])
@token_required
@role_required('admin')
@swag_from({
    'tags': ['Module'],
    'description': 'Create a new module.',
    'parameters': [
        {
            'name': 'name',
            'in': 'body',
            'type': 'string',
            'required': True,
            'description': 'The name of the module',
        },
        {
            'name': 'name_en',
            'in': 'body',
            'type': 'string',
            'required': False,
            'description': 'The English name of the module',
        },
        {
            'name': 'nature',
            'in': 'body',
            'type': 'string',
            'required': False,
            'description': 'The nature of the module',
        },
        {
            'name': 'category',
            'in': 'body',
            'type': 'string',
            'required': False,
            'description': 'The category of the module',
        },
        {
            'name': 'number',
            'in': 'body',
            'type': 'string',
            'required': False,
            'description': 'The serial number of the module',
        },
        {
            'name': 'credit',
            'in': 'body',
            'type': 'number',
            'required': False,
            'description': 'The credit of the module',
        },
        {
            'name': 'lec_hours',
            'in': 'body',
            'type': 'integer',
            'required': False,
            'description': 'The lecture hours of the module',
        },
        {
            'name': 'lab_hours',
            'in': 'body',
            'type': 'integer',
            'required': False,
            'description': 'The laboratory hours of the module',
        },
        {
            'name': 'oncampus_prac',
            'in': 'body',
            'type': 'integer',
            'required': False,
            'description': 'The on-campus practical hours of the module',
        },
        {
            'name': 'offcampus_prac',
            'in': 'body',
            'type': 'integer',
            'required': False,
            'description': 'The off-campus practical hours of the module',
        },
        {
            'name': 'term',
            'in': 'body',
            'type': 'string',
            'required': False,
            'description': 'The term in which the module is offered',
        },
        {
            'name': 'offered_by',
            'in': 'body',
            'type': 'string',
            'required': False,
            'description': 'The department/institute that offers the module',
        },
        {
            'name': 'description',
            'in': 'body',
            'type': 'string',
            'required': False,
            'description': 'The description of the module',
        },
        {
            'name': 'program_id',
            'in': 'body',
            'type': 'integer',
            'required': True,
            'description': 'ID of the program the module belongs to',
        }
    ],
    'responses': {
        201: {
            'description': 'Module created successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'module_id': {
                        'type': 'integer',
                        'description': 'The unique identifier of the module',
                    },
                    'name': {
                        'type': 'string'
                    },
                    'name_en': {
                        'type': 'string'
                    },
                    'nature': {
                        'type': 'string'
                    },
                    'category': {
                        'type': 'string'
                    },
                    'number': {
                        'type': 'string'
                    },
                    'credit': {
                        'type': 'number'
                    },
                    'lec_hours': {
                        'type': 'number'
                    },
                    'lab_hours': {
                        'type': 'number'
                    },
                    'oncampus_prac': {
                        'type': 'number'
                    },
                    'offcampus_prac': {
                        'type': 'number'
                    },
                    'term': {
                        'type': 'string'
                    },
                    'offered_by': {
                        'type': 'string'
                    },
                    'description': {
                        'type': 'string'
                    },
                    'program_id': {
                        'type': 'number'
                    },
                },
            },
        },
        400: {
            'description': 'Invalid input, object invalid',
        },
    },
})
def create_module(current_user):
    data = request.get_json()
    name = data.get('name')
    name_en = data.get('name_en')
    nature = data.get('nature')
    category = data.get('category')
    number = data.get('number')
    credit = data.get('credit')
    lec_hours = data.get('lec_hours')
    lab_hours = data.get('lab_hours')
    oncampus_prac = data.get('oncampus_prac')
    offcampus_prac = data.get('offcampus_prac')
    term = data.get('term')
    offered_by = data.get('offered_by')
    description = data.get('description')
    program_id = data.get('program_id')

    # Validate the required fields
    if not name or not program_id:
        return jsonify(message='Name and program ID are required'), 400

    # Validate program_id
    if not Program.query.get(program_id):
        return jsonify(message='Program ID is invalid or does not exist'), 400

    new_module = Module(
        name=name,
        name_en=name_en,
        nature=nature,
        category=category,
        number=number,
        credit=credit,
        lec_hours=lec_hours,
        lab_hours=lab_hours,
        oncampus_prac=oncampus_prac,
        offcampus_prac=offcampus_prac,
        term=term,
        offered_by=offered_by,
        description=description,
        program_id=program_id
    )
    db.session.add(new_module)
    db.session.commit()

    return jsonify({
        'module_id': new_module.module_id,
        'name': new_module.name,
        'name_en': new_module.name_en,
        'nature': new_module.nature,
        'category': new_module.category,
        'number': new_module.number,
        'credit': str(new_module.credit),
        'lec_hours': new_module.lec_hours,
        'lab_hours': new_module.lab_hours,
        'oncampus_prac': new_module.oncampus_prac,
        'offcampus_prac': new_module.offcampus_prac,
        'term': new_module.term,
        'offered_by': new_module.offered_by,
        'description': new_module.description,
        'program_id': new_module.program_id
    }), 201


@module_bp.route('/<int:module_id>', methods=['GET'])
@token_required
@role_required('staff')
@swag_from({
    'tags': ['Module'],
    'description': 'Get details of a specific module by ID.',
    'parameters': [
        {
            'name': 'module_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'The unique identifier of the module',
        },
    ],
    'responses': {
        200: {
            'description': 'Details of the module',
            'schema': {
                'type': 'object',
                'properties': {
                    'module_id': {
                        'type': 'integer',
                        'description': 'The unique identifier of the module',
                    },
                    'name': {
                        'type': 'string',
                        'description': 'The name of the module',
                    },
                    # Include other fields
                },
            },
        },
        404: {
            'description': 'Module not found',
        },
    },
})
def get_module(current_user, module_id: int):
    module = Module.query.get(module_id)
    if module:
        return jsonify({
            'module_id': module.module_id,
            'name': module.name,
            'name_en': module.name_en,
            'nature': module.nature,
            'category': module.category,
            'number': module.number,
            'credit': str(module.credit),
            'lec_hours': module.lec_hours,
            'lab_hours': module.lab_hours,
            'oncampus_prac': module.oncampus_prac,
            'offcampus_prac': module.offcampus_prac,
            'term': module.term,
            'offered_by': module.offered_by or '',
            'description': module.description,
            'program_id': module.program_id
        }), 200
    else:
        return jsonify(message='Module not found'), 404


@module_bp.route('/<int:module_id>', methods=['PUT'])
@token_required
@role_required('admin')
@swag_from({
    'tags': ['Module'],
    'description': 'Update an existing module by ID.',
    'parameters': [
        {
            'name': 'module_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'The unique identifier of the module to update',
        },
        {
            'name': 'body',
            'in': 'body',
            'description': 'Module object that needs to be updated',
            'required': True,
            'schema': {
                '$ref': '#/definitions/ModuleUpdate'
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Module updated successfully',
        },
        404: {
            'description': 'Module not found',
        },
    },
    'definitions': {
        'ModuleUpdate': {
            'type': 'object',
            'properties': {
                'name': {
                    'type': 'string',
                },
                'name': {
                    'type': 'string'
                },
                'name_en': {
                    'type': 'string'
                },
                'nature': {
                    'type': 'string'
                },
                'category': {
                    'type': 'string'
                },
                'number': {
                    'type': 'string'
                },
                'credit': {
                    'type': 'number'
                },
                'lec_hours': {
                    'type': 'number'
                },
                'lab_hours': {
                    'type': 'number'
                },
                'oncampus_prac': {
                    'type': 'number'
                },
                'offcampus_prac': {
                    'type': 'number'
                },
                'term': {
                    'type': 'string'
                },
                'offered_by': {
                    'type': 'string'
                },
                'description': {
                    'type': 'string'
                },
                'program_id': {
                    'type': 'number'
                },
            }
        }
    }
})
def update_module(current_user, module_id: int):
    module = Module.query.get(module_id)
    if not module:
        return jsonify(message='Module not found'), 404

    data = request.get_json()
    program_id = data.get('program_id')

    # Validate program_id
    if program_id and not Program.query.get(program_id):
        return jsonify(message='Program ID is invalid or does not exist'), 400

    # Update module details, checking for provided data
    module.name = data.get('name', module.name)
    module.name_en = data.get('name_en', module.name_en)
    module.nature = data.get('nature', module.nature)
    module.category = data.get('category', module.category)
    module.number = data.get('number', module.number)
    module.credit = data.get('credit', module.credit)
    module.lec_hours = data.get('lec_hours', module.lec_hours)
    module.lab_hours = data.get('lab_hours', module.lab_hours)
    module.oncampus_prac = data.get('oncampus_prac', module.oncampus_prac)
    module.offcampus_prac = data.get('offcampus_prac', module.offcampus_prac)
    module.term = data.get('term', module.term)
    module.offered_by = data.get('offered_by', module.offered_by)
    module.description = data.get('description', module.description)
    module.program_id = data.get('program_id', module.program_id)
    db.session.commit()

    return jsonify(message='Module updated successfully'), 200


@module_bp.route('/<int:module_id>', methods=['DELETE'])
@token_required
@role_required('admin')
@swag_from({
    'tags': ['Module'],
    'description': 'Delete a module by its ID.',
    'parameters': [
        {
            'name': 'module_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'The unique identifier of the module to delete',
        }
    ],
    'responses': {
        200: {
            'description': 'Module deleted successfully',
        },
        404: {
            'description': 'Module not found',
        },
    }
})
def delete_module(current_user, module_id: int):
    module = Module.query.get(module_id)
    if not module:
        return jsonify(message='Module not found'), 404

    db.session.delete(module)
    db.session.commit()

    return jsonify(message='Module deleted successfully'), 200


@module_bp.route('', methods=['GET'])
@token_required
@role_required('staff')
@swag_from({
    'tags': ['Module'],
    'description': 'Retrieve a list of all modules',
    'parameters': [
        {
            'name': 'name',
            'in': 'query',
            'type': 'string',
            'required': False,
            'description': 'Filter by module name',
        },
        {
            'name': 'offered_by',
            'in': 'query',
            'type': 'string',
            'required': False,
            'description': 'Filter by offering department',
        },
        # Add more filters as required
    ],
    'responses': {
        200: {
            'description': 'A list of modules',
            'schema': {
                'type': 'object',
                'properties': {
                    'modules': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'module_id': {
                                    'type': 'integer'
                                },
                                'name': {
                                    'type': 'string'
                                },
                                'name_en': {
                                    'type': 'string'
                                },
                                'nature': {
                                    'type': 'string'
                                },
                                'category': {
                                    'type': 'string'
                                },
                                'number': {
                                    'type': 'string'
                                },
                                'credit': {
                                    'type': 'number'
                                },
                                'lec_hours': {
                                    'type': 'number'
                                },
                                'lab_hours': {
                                    'type': 'number'
                                },
                                'oncampus_prac': {
                                    'type': 'number'
                                },
                                'offcampus_prac': {
                                    'type': 'number'
                                },
                                'term': {
                                    'type': 'string'
                                },
                                'offered_by': {
                                    'type': 'string'
                                },
                                'description': {
                                    'type': 'string'
                                },
                                'program_id': {
                                    'type': 'number'
                                },
                            },
                        },
                    },
                },
            },
        },
    }
})
def list_modules(current_user):
    query = Module.query
    name = request.args.get('name')
    offered_by = request.args.get('offered_by')

    if name:
        query = query.filter(Module.name.ilike(f'%{name}%'))
    if offered_by:
        query = query.filter(Module.offered_by.ilike(f'%{offered_by}%'))

    modules = query.all()
    modules_list = [{
        'module_id': mod.module_id,
        'name': mod.name,
        'name_en': mod.name_en,
        'nature': mod.nature,
        'category': mod.category,
        'number': mod.number,
        'credit': mod.credit,
        'lec_hours': mod.lec_hours,
        'lab_hours': mod.lab_hours,
        'oncampus_prac': mod.oncampus_prac,
        'offcampus_prac': mod.offcampus_prac,
        'term': mod.term,
        'offered_by': mod.offered_by or '',
        'description': mod.description,
        'program_id': mod.program_id,
    } for mod in modules]

    return jsonify(modules=modules_list), 200
