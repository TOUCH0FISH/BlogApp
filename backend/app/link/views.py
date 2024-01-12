from flask import Blueprint, request, jsonify
from app import db
from app.models.models import Module, Observation, ModObsRel
from flasgger import swag_from
from app.common.decorators import token_required, role_required

link_bp = Blueprint('link_bp', __name__)


@link_bp.route('/links', methods=['POST'])
@token_required
@role_required('admin')
@swag_from({
    'tags': ['Link'],
    'description': 'Create or update a link between an observation and a module with a specified weight. \
                    If the link already exists, it will update the weight. Otherwise, it will create a new link.',
    'parameters': [
        {
            'name': 'observation_id',
            'in': 'body',
            'type': 'integer',
            'required': True,
            'description': 'The ID of the observation'
        },
        {
            'name': 'module_id',
            'in': 'body',
            'type': 'integer',
            'required': True,
            'description': 'The ID of the module'
        },
        {
            'name': 'weight',
            'in': 'body',
            'type': 'integer',
            'required': False,
            'description': 'The weight of the link',
            'default': 1
        }
    ],
    'responses': {
        201: {
            'description': 'Link created',
            'schema': {
                'type': 'object',
                'properties': {
                    'mod_obs_id': {'type': 'integer'},
                    'observation_id': {'type': 'integer'},
                    'module_id': {'type': 'integer'},
                    'weight': {'type': 'integer'}
                }
            }
        },
        200: {
            'description': 'Link updated',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string'}
                }
            }
        },
        400: {
            'description': 'Invalid or non-existent observation or module ID',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string'}
                }
            }
        }
    }
})
def create_or_update_link(current_user):
    data = request.get_json()
    observation_id = data.get('observation_id')
    module_id = data.get('module_id')
    weight = data.get('weight', 1)

    # Check if the observation and module exist
    if not Observation.query.get(observation_id):
        return jsonify(message='Observation ID is invalid or does not exist'), 400
    if not Module.query.get(module_id):
        return jsonify(message='Module ID is invalid or does not exist'), 400

    # Check if the link already exists
    link = ModObsRel.query.filter_by(
        observation_id=observation_id, module_id=module_id).first()

    if link:
        # Update the existing link
        link.weight = weight
        db.session.commit()
        return jsonify(message='Link updated'), 200
    else:
        # Create a new link
        new_link = ModObsRel(
            observation_id=observation_id, module_id=module_id, weight=weight)
        db.session.add(new_link)
        db.session.commit()
        return jsonify({
            'mod_obs_id': new_link.mod_obs_id,
            'observation_id': new_link.observation_id,
            'module_id': new_link.module_id,
            'weight': new_link.weight
        }), 201


@link_bp.route('/links/<int:mod_obs_id>', methods=['GET'])
@token_required
@role_required('staff')
@swag_from({
    'tags': ['Link'],
    'description': 'Retrieve a specific link between a module and an observation by its ID.',
    'parameters': [
        {
            'name': 'mod_obs_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'The unique identifier of the module-observation link'
        }
    ],
    'responses': {
        200: {
            'description': 'A single link retrieved',
            'schema': {
                'type': 'object',
                'properties': {
                    'mod_obs_id': {'type': 'integer'},
                    'observation_id': {'type': 'integer'},
                    'module_id': {'type': 'integer'},
                    'weight': {'type': 'integer'}
                }
            }
        },
        404: {
            'description': 'Link not found',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string'}
                }
            }
        }
    }
})
def get_link(current_user, mod_obs_id: int):
    attr_obj_rel = ModObsRel.query.get(mod_obs_id)
    if attr_obj_rel:
        return jsonify({
            'mod_obs_id': attr_obj_rel.mod_obs_id,
            'observation_id': attr_obj_rel.observation_id,
            'module_id': attr_obj_rel.module_id,
            'weight': attr_obj_rel.weight
        }), 200
    else:
        return jsonify(message='Link not found'), 404


@link_bp.route('/links/<int:mod_obs_id>', methods=['DELETE'])
@token_required
@role_required('admin')
@swag_from({
    'tags': ['Link'],
    'description': 'Delete a specific link between a module and an observation by its ID.',
    'parameters': [
        {
            'name': 'mod_obs_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'The unique identifier of the module-observation link to be deleted'
        }
    ],
    'responses': {
        200: {
            'description': 'Link deleted successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string'}
                }
            }
        },
        404: {
            'description': 'Link not found',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string'}
                }
            }
        }
    }
})
def delete_link(current_user, mod_obs_id: int):
    attr_obj_rel = ModObsRel.query.get(mod_obs_id)
    if attr_obj_rel:
        db.session.delete(attr_obj_rel)
        db.session.commit()
        return jsonify(message='Link deleted'), 200
    else:
        return jsonify(message='Link not found'), 404


@link_bp.route('/links', methods=['GET'])
@token_required
@role_required('staff')
@swag_from({
    'tags': ['Link'],
    'description': 'List all link or filter by specific observation or module ID.',
    'parameters': [
        {
            'name': 'observation_id',
            'in': 'query',
            'type': 'integer',
            'required': False,
            'description': 'Filter by a specific observation ID'
        },
        {
            'name': 'module_id',
            'in': 'query',
            'type': 'integer',
            'required': False,
            'description': 'Filter by a specific module ID'
        }
    ],
    'responses': {
        200: {
            'description': 'List of links',
            'schema': {
                'type': 'object',
                'properties': {
                    'links': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'mod_obs_id': {'type': 'integer'},
                                'observation_id': {'type': 'integer'},
                                'module_id': {'type': 'integer'},
                                'weight': {'type': 'integer'}
                            }
                        }
                    }
                }
            }
        }
    }
})
def list_links(current_user):
    observation_id = request.args.get('observation_id')
    module_id = request.args.get('module_id')
    query = ModObsRel.query

    if observation_id:
        query = query.filter(ModObsRel.observation_id == observation_id)
    if module_id:
        query = query.filter(ModObsRel.module_id == module_id)

    links = query.all()
    links_list = [{
        'mod_obs_id': rel.mod_obs_id,
        'observation_id': rel.observation_id,
        'module_id': rel.module_id,
        'weight': rel.weight
    } for rel in links]

    return jsonify(links=links_list), 200


@link_bp.route('/modules/<int:module_id>/supports', methods=['POST'])
@token_required
@role_required('admin')
@swag_from({
    'tags': ['Module'],
    'description': 'Create or update supports for a module. If a link already exists, it will be updated.',
    'parameters': [
        {
            'name': 'module_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'The ID of the module to create or update supports for'
        },
        {
            'name': 'observations',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'observations': {
                        'type': 'array',
                        'description': 'An array of observations with their weights',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'observation_id': {
                                    'type': 'integer',
                                    'description': 'The ID of the observation'
                                },
                                'weight': {
                                    'type': 'integer',
                                    'description': 'The weight of the support',
                                    'default': 1
                                }
                            },
                            'required': ['observation_id']
                        }
                    }
                }
            }
        }
    ],
    'responses': {
        201: {
            'description': 'Supports for the module were created or updated successfully'
        },
        400: {
            'description': 'Invalid input, missing observations data'
        }
    }
})
def create_or_update_module_supports(current_user, module_id: int):
    data = request.get_json()
    observations = data.get('observations')

    if not observations:
        return jsonify(message='Observations data is required'), 400

    for obj in observations:
        # Check for existing link
        existing_link = ModObsRel.query.filter_by(
            observation_id=obj['observation_id'],
            module_id=module_id
        ).first()

        if existing_link:
            # Update existing link
            existing_link.weight = obj.get(
                'weight', existing_link.weight)
        else:
            # Create new link
            new_link = ModObsRel(
                observation_id=obj['observation_id'],
                module_id=module_id,
                weight=obj.get('weight', 1)
            )
            db.session.add(new_link)

    db.session.commit()
    return jsonify(message='Supports created or updated successfully'), 201


@link_bp.route('/modules/<int:module_id>/supports', methods=['GET'])
@token_required
@role_required('staff')
@swag_from({
    'tags': ['Module'],
    'description': 'Retrieve all links (supports) for a given module.',
    'parameters': [
        {
            'name': 'module_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'The ID of the module to retrieve supports for'
        }
    ],
    'responses': {
        200: {
            'description': 'A list of all supports for the module',
            'schema': {
                'type': 'object',
                'properties': {
                    'supports': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'mod_obs_id': {'type': 'integer'},
                                'observation_id': {'type': 'integer'},
                                'module_id': {'type': 'integer'},
                                'weight': {'type': 'integer'}
                            }
                        }
                    }
                }
            }
        }
    }
})
def get_module_supports(current_user, module_id):
    supports = ModObsRel.query.filter_by(module_id=module_id).all()
    supports_data = [{
        'mod_obs_id': support.mod_obs_id,
        'observation_id': support.observation_id,
        'module_id': support.module_id,
        'weight': support.weight
    } for support in supports]

    return jsonify(supports=supports_data), 200


@link_bp.route('/modules/<int:module_id>/supports', methods=['DELETE'])
@token_required
@role_required('admin')
@swag_from({
    'tags': ['Module'],
    'description': 'Delete all supports for a given module.',
    'parameters': [
        {
            'name': 'module_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'The ID of the module for which to delete supports'
        }
    ],
    'responses': {
        200: {
            'description': 'All supports for the module were deleted successfully'
        }
    }
})
def delete_module_supports(current_user, module_id: int):
    ModObsRel.query.filter_by(module_id=module_id).delete()
    db.session.commit()
    return jsonify(message='Supports deleted successfully'), 200


@link_bp.route('/observations/<int:observation_id>/supported-by', methods=['POST'])
@token_required
@role_required('admin')
@swag_from({
    'tags': ['Observation'],
    'description': 'Create or update links where an observation is supported by multiple modules.',
    'parameters': [
        {
            'name': 'observation_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'The ID of the observation to create or update support links for'
        },
        {
            'name': 'modules',
            'in': 'body',
            'type': 'array',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'module_id': {'type': 'integer'},
                    'weight': {'type': 'integer', 'default': 1}
                }
            },
            'description': 'Array of module objects containing the module ID and the weight of support'
        }
    ],
    'responses': {
        200: {
            'description': 'Supported by links were created or updated successfully'
        },
        400: {
            'description': 'Invalid input, object invalid'
        }
    }
})
def create_or_update_observation_supported_by(current_user, observation_id: int):
    data = request.get_json()
    modules = data.get('modules')

    if not modules:
        return jsonify(message='Modules data is required'), 400

    for attr in modules:
        link = ModObsRel.query.filter_by(
            observation_id=observation_id,
            module_id=attr['module_id']
        ).first()

        if link:
            # Update the existing link
            link.weight = attr.get('weight', 1)
        else:
            # Create a new link
            new_link = ModObsRel(
                observation_id=observation_id,
                module_id=attr['module_id'],
                weight=attr.get('weight', 1)
            )
            db.session.add(new_link)

    db.session.commit()
    return jsonify(message='Supported by links created or updated successfully'), 201


@link_bp.route('/observations/<int:observation_id>/supported-by', methods=['GET'])
@token_required
@role_required('staff')
@swag_from({
    'tags': ['Observation'],
    'description': 'List all links where an observation is supported by modules.',
    'parameters': [
        {
            'name': 'observation_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'The ID of the observation to retrieve support links for'
        }
    ],
    'responses': {
        200: {
            'description': 'List of links supporting the observation',
            'schema': {
                'type': 'object',
                'properties': {
                    'links': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'mod_obs_id': {'type': 'integer'},
                                'observation_id': {'type': 'integer'},
                                'module_id': {'type': 'integer'},
                                'weight': {'type': 'integer'}
                            }
                        }
                    }
                }
            }
        },
        404: {
            'description': 'Observation not found'
        }
    }
})
def get_observation_supported_by(current_user, observation_id: int):
    links = ModObsRel.query.filter_by(observation_id=observation_id).all()
    links_list = [{
        'mod_obs_id': link.mod_obs_id,
        'observation_id': link.observation_id,
        'module_id': link.module_id,
        'weight': link.weight
    } for link in links]

    if not links_list:
        return jsonify(message='No links found for this observation'), 404

    return jsonify(links=links_list), 200


@link_bp.route('/observations/<int:observation_id>/supported-by', methods=['DELETE'])
@token_required
@role_required('admin')
@swag_from({
    'tags': ['Observation'],
    'description': 'Delete all links where an observation is supported by modules.',
    'parameters': [
        {
            'name': 'observation_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'The ID of the observation to delete support links for'
        }
    ],
    'responses': {
        200: {
            'description': 'Supported by links were deleted successfully'
        },
        400: {
            'description': 'Invalid input, object invalid'
        }
    }
})
def delete_observation_supported_by(current_user, observation_id: int):
    ModObsRel.query.filter_by(observation_id=observation_id).delete()
    db.session.commit()
    return jsonify(message='Supported by links deleted successfully'), 200
