from flask import Blueprint, request, jsonify
from app import db
from app.models.models import Attribute, Objective, AttrObjRel
from flasgger import swag_from
from app.common.decorators import token_required, role_required

relation_bp = Blueprint('relation_bp', __name__)


@relation_bp.route('/relations', methods=['POST'])
@token_required
@role_required('admin')
@swag_from({
    'tags': ['Relation'],
    'description': 'Create or update a relationship between an attribute and an objective with a specified weight. \
                    If the relationship already exists, it will update the weight. Otherwise, it will create a new relationship.',
    'parameters': [
        {
            'name': 'objective_id',
            'in': 'body',
            'type': 'integer',
            'required': True,
            'description': 'The ID of the objective'
        },
        {
            'name': 'attribute_id',
            'in': 'body',
            'type': 'integer',
            'required': True,
            'description': 'The ID of the attribute'
        },
        {
            'name': 'weight',
            'in': 'body',
            'type': 'integer',
            'required': False,
            'description': 'The weight of the relationship',
            'default': 1
        }
    ],
    'responses': {
        201: {
            'description': 'Relation created',
            'schema': {
                'type': 'object',
                'properties': {
                    'attr_obj_id': {'type': 'integer'},
                    'objective_id': {'type': 'integer'},
                    'attribute_id': {'type': 'integer'},
                    'weight': {'type': 'integer'}
                }
            }
        },
        200: {
            'description': 'Relation updated',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string'}
                }
            }
        },
        400: {
            'description': 'Invalid or non-existent objective or attribute ID',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string'}
                }
            }
        }
    }
})
def create_or_update_relation(current_user):
    data = request.get_json()
    objective_id = data.get('objective_id')
    attribute_id = data.get('attribute_id')
    weight = data.get('weight', 1)

    # Check if the objective and attribute exist
    if not Objective.query.get(objective_id):
        return jsonify(message='Objective ID is invalid or does not exist'), 400
    if not Attribute.query.get(attribute_id):
        return jsonify(message='Attribute ID is invalid or does not exist'), 400

    # Check if the relation already exists
    relation = AttrObjRel.query.filter_by(
        objective_id=objective_id, attribute_id=attribute_id).first()

    if relation:
        # Update the existing relation
        relation.weight = weight
        db.session.commit()
        return jsonify(message='Relation updated'), 200
    else:
        # Create a new relation
        new_relation = AttrObjRel(
            objective_id=objective_id, attribute_id=attribute_id, weight=weight)
        db.session.add(new_relation)
        db.session.commit()
        return jsonify({
            'attr_obj_id': new_relation.attr_obj_id,
            'objective_id': new_relation.objective_id,
            'attribute_id': new_relation.attribute_id,
            'weight': new_relation.weight
        }), 201


@relation_bp.route('/relations/<int:attr_obj_id>', methods=['GET'])
@token_required
@role_required('staff')
@swag_from({
    'tags': ['Relation'],
    'description': 'Retrieve a specific relationship between an attribute and an objective by its ID.',
    'parameters': [
        {
            'name': 'attr_obj_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'The unique identifier of the attribute-objective relationship'
        }
    ],
    'responses': {
        200: {
            'description': 'A single relation retrieved',
            'schema': {
                'type': 'object',
                'properties': {
                    'attr_obj_id': {'type': 'integer'},
                    'objective_id': {'type': 'integer'},
                    'attribute_id': {'type': 'integer'},
                    'weight': {'type': 'integer'}
                }
            }
        },
        404: {
            'description': 'Relation not found',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string'}
                }
            }
        }
    }
})
def get_relation(current_user, attr_obj_id: int):
    attr_obj_rel = AttrObjRel.query.get(attr_obj_id)
    if attr_obj_rel:
        return jsonify({
            'attr_obj_id': attr_obj_rel.attr_obj_id,
            'objective_id': attr_obj_rel.objective_id,
            'attribute_id': attr_obj_rel.attribute_id,
            'weight': attr_obj_rel.weight
        }), 200
    else:
        return jsonify(message='Relation not found'), 404


@relation_bp.route('/relations/<int:attr_obj_id>', methods=['DELETE'])
@token_required
@role_required('admin')
@swag_from({
    'tags': ['Relation'],
    'description': 'Delete a specific relationship between an attribute and an objective by its ID.',
    'parameters': [
        {
            'name': 'attr_obj_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'The unique identifier of the attribute-objective relationship to be deleted'
        }
    ],
    'responses': {
        200: {
            'description': 'Relation deleted successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string'}
                }
            }
        },
        404: {
            'description': 'Relation not found',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string'}
                }
            }
        }
    }
})
def delete_relation(current_user, attr_obj_id: int):
    attr_obj_rel = AttrObjRel.query.get(attr_obj_id)
    if attr_obj_rel:
        db.session.delete(attr_obj_rel)
        db.session.commit()
        return jsonify(message='Relation deleted'), 200
    else:
        return jsonify(message='Relation not found'), 404


@relation_bp.route('/relations', methods=['GET'])
@token_required
@role_required('staff')
@swag_from({
    'tags': ['Relation'],
    'description': 'List all relationships or filter by specific objective or attribute ID.',
    'parameters': [
        {
            'name': 'objective_id',
            'in': 'query',
            'type': 'integer',
            'required': False,
            'description': 'Filter by a specific objective ID'
        },
        {
            'name': 'attribute_id',
            'in': 'query',
            'type': 'integer',
            'required': False,
            'description': 'Filter by a specific attribute ID'
        }
    ],
    'responses': {
        200: {
            'description': 'List of relations',
            'schema': {
                'type': 'object',
                'properties': {
                    'relations': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'attr_obj_id': {'type': 'integer'},
                                'objective_id': {'type': 'integer'},
                                'attribute_id': {'type': 'integer'},
                                'weight': {'type': 'integer'}
                            }
                        }
                    }
                }
            }
        }
    }
})
def list_relations(current_user):
    objective_id = request.args.get('objective_id')
    attribute_id = request.args.get('attribute_id')
    query = AttrObjRel.query

    if objective_id:
        query = query.filter(AttrObjRel.objective_id == objective_id)
    if attribute_id:
        query = query.filter(AttrObjRel.attribute_id == attribute_id)

    relations = query.all()
    relations_list = [{
        'attr_obj_id': rel.attr_obj_id,
        'objective_id': rel.objective_id,
        'attribute_id': rel.attribute_id,
        'weight': rel.weight
    } for rel in relations]

    return jsonify(relations=relations_list), 200


@relation_bp.route('/graduate-attributes/<int:attribute_id>/supports', methods=['POST'])
@token_required
@role_required('admin')
@swag_from({
    'tags': ['Graduate Attribute'],
    'description': 'Create or update supports for a graduate attribute. If a relation already exists, it will be updated.',
    'parameters': [
        {
            'name': 'attribute_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'The ID of the graduate attribute to create or update supports for'
        },
        {
            'name': 'objectives',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'objectives': {
                        'type': 'array',
                        'description': 'An array of objectives with their weights',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'objective_id': {
                                    'type': 'integer',
                                    'description': 'The ID of the objective'
                                },
                                'weight': {
                                    'type': 'integer',
                                    'description': 'The weight of the support',
                                    'default': 1
                                }
                            },
                            'required': ['objective_id']
                        }
                    }
                }
            }
        }
    ],
    'responses': {
        201: {
            'description': 'Supports for the attribute were created or updated successfully'
        },
        400: {
            'description': 'Invalid input, missing objectives data'
        }
    }
})
def create_or_update_attribute_supports(current_user, attribute_id: int):
    data = request.get_json()
    objectives = data.get('objectives')

    if not objectives:
        return jsonify(message='Objectives data is required'), 400

    for obj in objectives:
        # Check for existing relation
        existing_relation = AttrObjRel.query.filter_by(
            objective_id=obj['objective_id'],
            attribute_id=attribute_id
        ).first()

        if existing_relation:
            # Update existing relation
            existing_relation.weight = obj.get(
                'weight', existing_relation.weight)
        else:
            # Create new relation
            new_relation = AttrObjRel(
                objective_id=obj['objective_id'],
                attribute_id=attribute_id,
                weight=obj.get('weight', 1)
            )
            db.session.add(new_relation)

    db.session.commit()
    return jsonify(message='Supports created or updated successfully'), 201


@relation_bp.route('/graduate-attributes/<int:attribute_id>/supports', methods=['GET'])
@token_required
@role_required('staff')
@swag_from({
    'tags': ['Graduate Attribute'],
    'description': 'Retrieve all relations (supports) for a given graduate attribute.',
    'parameters': [
        {
            'name': 'attribute_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'The ID of the graduate attribute to retrieve supports for'
        }
    ],
    'responses': {
        200: {
            'description': 'A list of all supports for the attribute',
            'schema': {
                'type': 'object',
                'properties': {
                    'supports': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'attr_obj_id': {'type': 'integer'},
                                'objective_id': {'type': 'integer'},
                                'attribute_id': {'type': 'integer'},
                                'weight': {'type': 'integer'}
                            }
                        }
                    }
                }
            }
        }
    }
})
def get_attribute_supports(current_user, attribute_id):
    supports = AttrObjRel.query.filter_by(attribute_id=attribute_id).all()
    supports_data = [{
        'attr_obj_id': support.attr_obj_id,
        'objective_id': support.objective_id,
        'attribute_id': support.attribute_id,
        'weight': support.weight
    } for support in supports]

    return jsonify(supports=supports_data), 200


@relation_bp.route('/graduate-attributes/<int:attribute_id>/supports', methods=['DELETE'])
@token_required
@role_required('admin')
@swag_from({
    'tags': ['Graduate Attribute'],
    'description': 'Delete all supports for a given graduate attribute.',
    'parameters': [
        {
            'name': 'attribute_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'The ID of the graduate attribute for which to delete supports'
        }
    ],
    'responses': {
        200: {
            'description': 'All supports for the attribute were deleted successfully'
        }
    }
})
def delete_attribute_supports(current_user, attribute_id: int):
    AttrObjRel.query.filter_by(attribute_id=attribute_id).delete()
    db.session.commit()
    return jsonify(message='Supports deleted successfully'), 200


@relation_bp.route('/objectives/<int:objective_id>/supported-by', methods=['POST'])
@token_required
@role_required('admin')
@swag_from({
    'tags': ['Objective'],
    'description': 'Create or update relations where an objective is supported by multiple attributes.',
    'parameters': [
        {
            'name': 'objective_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'The ID of the objective to create or update support relations for'
        },
        {
            'name': 'attributes',
            'in': 'body',
            'type': 'array',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'attribute_id': {'type': 'integer'},
                    'weight': {'type': 'integer', 'default': 1}
                }
            },
            'description': 'Array of attribute objects containing the attribute ID and the weight of support'
        }
    ],
    'responses': {
        200: {
            'description': 'Supported by relations were created or updated successfully'
        },
        400: {
            'description': 'Invalid input, object invalid'
        }
    }
})
def create_or_update_objective_supported_by(current_user, objective_id: int):
    data = request.get_json()
    attributes = data.get('attributes')

    if not attributes:
        return jsonify(message='Attributes data is required'), 400

    for attr in attributes:
        relation = AttrObjRel.query.filter_by(
            objective_id=objective_id,
            attribute_id=attr['attribute_id']
        ).first()

        if relation:
            # Update the existing relation
            relation.weight = attr.get('weight', 1)
        else:
            # Create a new relation
            new_relation = AttrObjRel(
                objective_id=objective_id,
                attribute_id=attr['attribute_id'],
                weight=attr.get('weight', 1)
            )
            db.session.add(new_relation)

    db.session.commit()
    return jsonify(message='Supported by relations created or updated successfully'), 201


@relation_bp.route('/objectives/<int:objective_id>/supported-by', methods=['GET'])
@token_required
@role_required('staff')
@swag_from({
    'tags': ['Objective'],
    'description': 'List all relations where an objective is supported by attributes.',
    'parameters': [
        {
            'name': 'objective_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'The ID of the objective to retrieve support relations for'
        }
    ],
    'responses': {
        200: {
            'description': 'List of relations supporting the objective',
            'schema': {
                'type': 'object',
                'properties': {
                    'relations': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'attr_obj_id': {'type': 'integer'},
                                'objective_id': {'type': 'integer'},
                                'attribute_id': {'type': 'integer'},
                                'weight': {'type': 'integer'}
                            }
                        }
                    }
                }
            }
        },
        404: {
            'description': 'Objective not found'
        }
    }
})
def get_objective_supported_by(current_user, objective_id: int):
    relations = AttrObjRel.query.filter_by(objective_id=objective_id).all()
    relations_list = [{
        'attr_obj_id': rel.attr_obj_id,
        'objective_id': rel.objective_id,
        'attribute_id': rel.attribute_id,
        'weight': rel.weight
    } for rel in relations]

    if not relations_list:
        return jsonify(message='No relations found for this objective'), 404

    return jsonify(relations=relations_list), 200


@relation_bp.route('/objectives/<int:objective_id>/supported-by', methods=['DELETE'])
@token_required
@role_required('admin')
@swag_from({
    'tags': ['Objective'],
    'description': 'Delete all relations where an objective is supported by attributes.',
    'parameters': [
        {
            'name': 'objective_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'The ID of the objective to delete support relations for'
        }
    ],
    'responses': {
        200: {
            'description': 'Supported by relations were deleted successfully'
        },
        400: {
            'description': 'Invalid input, object invalid'
        }
    }
})
def delete_objective_supported_by(current_user, objective_id: int):
    AttrObjRel.query.filter_by(objective_id=objective_id).delete()
    db.session.commit()
    return jsonify(message='Supported by relations deleted successfully'), 200
