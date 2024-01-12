from flask import Blueprint, request, jsonify, current_app, send_from_directory
from app import db
from app.models.models import Material, Module, Tag
from app.common.local_storage import LocalFileManager
from app.common.decorators import token_required
from app.tasks import send_notification
from werkzeug.utils import secure_filename
from flasgger import swag_from
import os

material_bp = Blueprint('material', __name__, url_prefix='/materials')


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


@material_bp.route('', methods=['POST'])
@token_required
@swag_from({
    'tags': ['Material'],
    'consumes': ['multipart/form-data'],
    'parameters': [
        {
            'name': 'title',
            'in': 'formData',
            'type': 'string',
            'required': True,
            'description': 'The title of the material',
        },
        {
            'name': 'description',
            'in': 'formData',
            'type': 'string',
            'required': False,
            'description': 'A description of the material',
        },
        {
            'name': 'file',
            'in': 'formData',
            'type': 'file',
            'required': True,
            'description': 'The file to upload',
        },
        {
            'name': 'module_id',
            'in': 'formData',
            'type': 'integer',
            'required': True,
            'description': 'ID of the associated module',
        },
        {
            'name': 'tag_id',
            'in': 'formData',
            'type': 'integer',
            'required': True,
            'description': 'ID of the associated tag',
        },
    ],
    'responses': {
        '201': {
            'description': 'Material created successfully',
            'schema': {
                'id': 'MaterialResponse',
                'properties': {
                    'material_id': {
                        'type': 'integer',
                        'description': 'The ID of the material'
                    },
                    'title': {
                        'type': 'string',
                        'description': 'The title of the material'
                    },
                    'description': {
                        'type': 'string',
                        'description': 'A description of the material'
                    },
                    'file_path': {
                        'type': 'string',
                        'description': 'The relative path to the material file'
                    },
                    'user_id': {
                        'type': 'integer',
                        'description': 'The ID of the user who owns the material'
                    },
                    'module_id': {
                        'type': 'integer',
                        'description': 'The ID of the module the material is associated with'
                    },
                    'tag_id': {
                        'type': 'integer',
                        'description': 'The ID of the tag associated with the material'
                    },
                    'created_at': {
                        'type': 'string',
                        'format': 'date-time',
                        'description': 'The creation date of the material'
                    },
                    'updated_at': {
                        'type': 'string',
                        'format': 'date-time',
                        'description': 'The last update date of the material'
                    }
                },
            },
        },
        '400': {
            'description': 'Invalid input',
        },
        '401': {
            'description': 'Unauthorized',
        },
        # Other responses...
    },
})
def create_material(current_user):
    # if 'file' not in request.files:
    #     return jsonify(message='No file part'), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify(message='No selected file'), 400
    if not allowed_file(file.filename):
        return jsonify(message='File type not allowed'), 400
    
    print(data)
    data = request.form
    title = data.get('title')
    description = data.get('description')
    module_id = data.get('module_id')
    tag_id = data.get('tag_id')

    # Validate module_id and tag_id

    # for testing
    print(f'Received module ID: {module_id}')
    module = Module.query.get(module_id)
    if not module:
        return jsonify(message='Module not found'), 404
    tag = Tag.query.get(tag_id)
    if not tag:
        return jsonify(message='Tag not found'), 404

    file_manager = LocalFileManager(current_app.config['UPLOAD_FOLDER'])
    filename = secure_filename(file.filename)
    relative_path = os.path.join(module.name, tag.name)
    full_path = file_manager.save(file, relative_path)

    new_material = Material(
        title=title,
        description=description,
        file_path=os.path.join(relative_path, filename),
        user_id=current_user.user_id,
        module_id=module_id,
        tag_id=tag_id
    )
    db.session.add(new_material)
    db.session.commit()

    # Trigger the Celery task
    send_notification.delay(
        current_user.user_id, f'New material uploaded: \n{module.name}\n{tag.name}\n{new_material.title}')

    return jsonify({
        'material_id': new_material.material_id,
        'title': new_material.title,
        'description': new_material.description,
        'file_path': new_material.file_path,
        'user_id': new_material.user_id,
        'module_id': new_material.module_id,
        'tag_id': new_material.tag_id,
        'created_at': new_material.created_at
    }), 201


@material_bp.route('/<int:material_id>', methods=['PUT'])
@token_required
@swag_from({
    'tags': ['Material'],
    'parameters': [
        {
            'name': 'title',
            'in': 'formData',
            'type': 'string',
            'description': 'The title of the material',
            'required': False
        },
        {
            'name': 'description',
            'in': 'formData',
            'type': 'string',
            'description': 'A description of the material',
            'required': False
        },
        {
            'name': 'module_id',
            'in': 'formData',
            'type': 'integer',
            'description': 'The ID of the module the material is associated with',
            'required': False
        },
        {
            'name': 'tag_id',
            'in': 'formData',
            'type': 'integer',
            'description': 'The ID of the tag associated with the material',
            'required': False
        },
        {
            'name': 'file',
            'in': 'formData',
            'type': 'file',
            'description': 'The file attachment for the material',
            'required': False
        }
    ],
    'responses': {
        '200': {
            'description': 'Material updated successfully',
            'schema': {
                'id': 'MaterialResponse',
                'properties': {
                    'material_id': {
                        'type': 'integer',
                        'description': 'The ID of the material'
                    },
                    'title': {
                        'type': 'string',
                        'description': 'The title of the material'
                    },
                    'description': {
                        'type': 'string',
                        'description': 'A description of the material'
                    },
                    'file_path': {
                        'type': 'string',
                        'description': 'The relative path to the material file'
                    },
                    'user_id': {
                        'type': 'integer',
                        'description': 'The ID of the user who owns the material'
                    },
                    'module_id': {
                        'type': 'integer',
                        'description': 'The ID of the module the material is associated with'
                    },
                    'tag_id': {
                        'type': 'integer',
                        'description': 'The ID of the tag associated with the material'
                    },
                    'created_at': {
                        'type': 'string',
                        'format': 'date-time',
                        'description': 'The creation date of the material'
                    },
                    'updated_at': {
                        'type': 'string',
                        'format': 'date-time',
                        'description': 'The last update date of the material'
                    }
                }
            }
        },
        '400': {
            'description': 'Bad request. Could be due to invalid input or file type not allowed.'
        },
        '403': {
            'description': 'Unauthorized. User does not have permission to update this material.'
        },
        '404': {
            'description': 'Material not found.'
        }
    },
    'consumes': ['multipart/form-data']
})
def update_material(current_user, material_id: int):
    material = Material.query.get(material_id)
    if not material:
        return jsonify(message='Material not found'), 404
    if material.user_id != current_user.user_id:
        return jsonify(message='Unauthorized'), 403

    data = request.form
    title = data.get('title')
    description = data.get('description')
    module_id = data.get('module_id')
    tag_id = data.get('tag_id')

    # Validate module_id and tag_id
    module = Module.query.get(module_id)
    if module_id and not module:
        return jsonify(message='Module not found'), 404
    tag = Tag.query.get(tag_id)
    if tag and not tag:
        return jsonify(message='Tag not found'), 404

    # Update other fields
    material.title = title if title else material.title
    material.description = description if description else material.description
    material.module_id = module_id if module_id else material.module_id
    material.tag_id = tag_id if tag_id else material.tag_id

    # Update the file if a new file is provided
    if 'file' in request.files and request.files['file'].filename != '':
        file = request.files['file']
        if not allowed_file(file.filename):
            return jsonify(message='File type not allowed'), 400

        file_manager = LocalFileManager(current_app.config['UPLOAD_FOLDER'])
        filename = secure_filename(file.filename)
        relative_path = os.path.join(Module.query.get(
            material.module_id).name, Tag.query.get(material.tag_id).name)
        # Delete the old file
        file_manager.delete(material.file_path)
        # Save the new file
        full_path = file_manager.save(file, relative_path)
        material.file_path = os.path.join(relative_path, filename)

    db.session.commit()

    # Trigger the Celery task
    send_notification.delay(
        current_user.user_id, f'The material is updated successfully: \n{Module.query.get(material.module_id).name}\n{Tag.query.get(material.tag_id).name}\n{material.title}')

    return jsonify({
        'material_id': material.material_id,
        'title': material.title,
        'description': material.description,
        'file_path': material.file_path,
        'user_id': material.user_id,
        'module_id': material.module_id,
        'tag_id': material.tag_id,
        'created_at': material.created_at,
        'updated_at': material.updated_at
    }), 200


@material_bp.route('/<int:material_id>', methods=['DELETE'])
@token_required
@swag_from({
    'tags': ['Material'],
    'description': 'Deletes a material with the given ID',
    'parameters': [
        {
            'name': 'material_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'Unique ID of the material to delete',
        },
    ],
    'responses': {
        '200': {
            'description': 'Material deleted successfully',
            'examples': {
                'application/json': {
                    'message': 'Material deleted successfully.'
                }
            }
        },
        '403': {
            'description': 'Unauthorized to delete this material',
            'examples': {
                'application/json': {
                    'message': 'Unauthorized to delete this material.'
                }
            }
        },
        '404': {
            'description': 'Material not found',
            'examples': {
                'application/json': {
                    'message': 'Material not found.'
                }
            }
        },
        '500': {
            'description': 'Failed to delete the associated file or database error',
            'examples': {
                'application/json': {
                    'message': 'Failed to delete the associated file.'
                }
            }
        }
    },
    'security': [
        {
            'BearerAuth': []
        }
    ]
})
def delete_material(current_user, material_id: int):
    material = Material.query.get(material_id)
    if not material:
        return jsonify({'message': 'Material not found.'}), 404

    # Validate module_id and tag_id
    module = Module.query.get(material.module_id)
    tag = Tag.query.get(material.tag_id)

    if current_user.user_id != material.user_id:
        return jsonify({'message': 'Unauthorized to delete this material.'}), 403

    # Delete the file from the filesystem
    file_manager = LocalFileManager(current_app.config['UPLOAD_FOLDER'])
    if not file_manager.delete(material.file_path):
        return jsonify({'message': 'Failed to delete the associated file.'}), 500

    # Delete the material from the database
    db.session.delete(material)
    db.session.commit()

    # Trigger the Celery task
    send_notification.delay(
        current_user.user_id, f'The material is deleted successfully: \n{module.name}\n{tag.name}\n{material.title}')

    return jsonify({'message': 'Material deleted successfully.'}), 200


@material_bp.route('/<int:material_id>', methods=['GET'])
@token_required
@swag_from({
    'tags': ['Material'],
    'parameters': [
        {
            'name': 'material_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'Unique ID of the material',
        }
    ],
    'responses': {
        '200': {
            'description': 'Details of the material',
            'schema': {
                'id': 'Material',
                'properties': {
                    'material_id': {
                        'type': 'integer',
                        'description': 'The ID of the material',
                    },
                    'title': {
                        'type': 'string',
                        'description': 'The title of the material',
                    },
                    'description': {
                        'type': 'string',
                        'description': 'The description of the material',
                    },
                    'file_path': {
                        'type': 'string',
                        'description': 'The path to the material file',
                    },
                    'user_id': {
                        'type': 'integer',
                        'description': 'The ID of the user who uploaded the material',
                    },
                    'module_id': {
                        'type': 'integer',
                        'description': 'The ID of the module this material is associated with',
                    },
                    'tag_id': {
                        'type': 'integer',
                        'description': 'The ID of the tag associated with the material',
                    },
                    'created_at': {
                        'type': 'string',
                        'format': 'date-time',
                        'description': 'The time when the material was created',
                    },
                    'updated_at': {
                        'type': 'string',
                        'format': 'date-time',
                        'description': 'The last time when the material was updated',
                    },
                }
            }
        },
        '404': {
            'description': 'Material not found',
        },
        '401': {
            'description': 'Unauthorized access - if the user is not logged in or does not have the right permissions',
        }
    }
})
def get_material(current_user, material_id: int):
    material = Material.query.get(material_id)
    if not material:
        return jsonify({'message': 'Material not found.'}), 404

    return jsonify(
        material_id=material.material_id,
        title=material.title,
        description=material.description,
        file_path=material.file_path,
        user_id=material.user_id,
        module_id=material.module_id,
        tag_id=material.tag_id,
        created_at=material.created_at,
        updated_at=material.updated_at), 200


@material_bp.route('', methods=['GET'])
@token_required
@swag_from({
    'tags': ['Material'],
    'parameters': [
        {
            'name': 'title',
            'in': 'query',
            'type': 'string',
            'description': 'Filter materials by title',
            'required': False
        },
        {
            'name': 'module_id',
            'in': 'query',
            'type': 'integer',
            'description': 'Filter materials by module ID',
            'required': False
        },
        {
            'name': 'tag_id',
            'in': 'query',
            'type': 'integer',
            'description': 'Filter materials by tag ID',
            'required': False
        }
    ],
    'responses': {
        '200': {
            'description': 'A list of materials',
            'schema': {
                'type': 'object',
                'properties': {
                    'materials': {
                        'type': 'array',
                        'items': {
                            '$ref': '#/definitions/Material'
                        }
                    }
                }
            }
        },
        '400': {
            'description': 'Invalid query parameters'
        },
        '401': {
            'description': 'Unauthorized. The user is not logged in or does not have permission to view the materials.'
        }
    }
})
def get_materials_list(current_user):
    materials_query = Material.query

    # Optional filters
    title_filter = request.args.get('title')
    module_id_filter = request.args.get('module_id')
    tag_id_filter = request.args.get('tag_id')

    if title_filter:
        materials_query = materials_query.filter(
            Material.title.ilike(f"%{title_filter}%"))
    if module_id_filter:
        materials_query = materials_query.filter_by(module_id=module_id_filter)
    if tag_id_filter:
        materials_query = materials_query.filter_by(tag_id=tag_id_filter)

    materials = materials_query.all()
    materials_data = [{
        'material_id': material.material_id,
        'title': material.title,
        'description': material.description,
        'file_path': material.file_path,
        'user_id': material.user_id,
        'module_id': material.module_id,
        'tag_id': material.tag_id,
        'created_at': material.created_at,
        'updated_at': material.updated_at
    } for material in materials]

    return jsonify(materials=materials_data), 200


@material_bp.route('/<int:material_id>/download', methods=['GET'])
@token_required
@swag_from({
    'tags': ['Material'],
    'parameters': [
        {
            'name': 'material_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'The ID of the material to download'
        }
    ],
    'responses': {
        '200': {
            'description': 'Material file is downloaded',
            'content': {
                'application/octet-stream': {
                    'example': 'Binary file content'
                }
            }
        },
        '404': {
            'description': 'Material not found or file not found'
        },
        '401': {
            'description': 'Unauthorized. The user is not logged in or does not have permission to download the material.'
        }
    },
    'security': [
        {
            'BearerAuth': []
        }
    ]
})
def download_material(current_user, material_id: int):
    material = Material.query.get(material_id)
    if not material:
        return jsonify({'message': 'Material not found.'}), 404

    try:
        return send_from_directory(
            directory=current_app.config['UPLOAD_FOLDER'],
            path=material.file_path,
            as_attachment=True
        )
    except FileNotFoundError:
        return jsonify({'message': 'File not found.'}), 404
