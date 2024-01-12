from flask import Blueprint, request, jsonify
from app import db
from app.models.models import Observation, Attribute
from flasgger import swag_from
from app.common.decorators import token_required, role_required

observation_bp = Blueprint('observation_bp', __name__,
                           url_prefix='/observations')


@observation_bp.route('', methods=['POST'])
@token_required
@role_required('admin')
@swag_from({
    'tags': ['Observation'],
    'description': 'Create a new observation for a given attribute.',
    'parameters': [
        {
            'name': 'name',
            'in': 'body',
            'type': 'string',
            'required': True,
            'description': 'The name of the observation'
        },
        {
            'name': 'description',
            'in': 'body',
            'type': 'string',
            'required': False,
            'description': 'A description of the observation'
        },
        {
            'name': 'attribute_id',
            'in': 'body',
            'type': 'integer',
            'required': True,
            'description': 'The ID of the attribute the observation is associated with'
        }
    ],
    'responses': {
        201: {
            'description': 'Observation created successfully'
        },
        400: {
            'description': 'Invalid input, object invalid'
        }
    }
})
def create_observation(current_user):
    data = request.get_json()
    name = data.get('name')
    description = data.get('description', '')
    attribute_id = data.get('attribute_id')

    if not name or not attribute_id:
        return jsonify(message='Name and attribute ID are required'), 400

    # Validate attribute_id
    if attribute_id and not Attribute.query.get(attribute_id):
        return jsonify(message='Attribute ID is invalid or does not exist'), 400

    new_observation = Observation(
        name=name, description=description, attribute_id=attribute_id)
    db.session.add(new_observation)
    db.session.commit()

    return jsonify({
        'observation_id': new_observation.observation_id,
        'name': new_observation.name,
        'description': new_observation.description,
        'attribute_id': new_observation.attribute_id
    }), 201


@observation_bp.route('/<int:observation_id>', methods=['GET'])
@token_required
@role_required('staff')
@swag_from({
    'tags': ['Observation'],
    'description': 'Get a specific observation by its ID.',
    'parameters': [
        {
            'name': 'observation_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'The ID of the observation to retrieve'
        }
    ],
    'responses': {
        200: {
            'description': 'Observation retrieved successfully'
        },
        404: {
            'description': 'Observation not found'
        }
    }
})
def get_observation(current_user, observation_id: int):
    observation = Observation.query.get(observation_id)
    if observation:
        return jsonify({
            'observation_id': observation.observation_id,
            'name': observation.name,
            'description': observation.description,
            'attribute_id': observation.attribute_id
        }), 200
    else:
        return jsonify(message='Observation not found'), 404


@observation_bp.route('/<int:observation_id>', methods=['PUT'])
@token_required
@role_required('admin')
@swag_from({
    'tags': ['Observation'],
    'description': 'Update an existing observation.',
    'parameters': [
        {
            'name': 'observation_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'The ID of the observation to update'
        },
        {
            'name': 'name',
            'in': 'body',
            'type': 'string',
            'required': False,
            'description': 'The new name of the observation'
        },
        {
            'name': 'description',
            'in': 'body',
            'type': 'string',
            'required': False,
            'description': 'The new description of the observation'
        },
        {
            'name': 'attribute_id',
            'in': 'body',
            'type': 'integer',
            'required': True,
            'description': 'The ID of the attribute the observation is associated with'
        }
    ],
    'responses': {
        200: {
            'description': 'Observation updated successfully'
        },
        404: {
            'description': 'Observation not found'
        }
    }
})
def update_observation(current_user, observation_id: int):
    observation = Observation.query.get(observation_id)
    if not observation:
        return jsonify(message='Observation not found'), 404

    data = request.get_json()
    attribute_id = data.get('attribute_id')

    # Validate attribute_id
    if attribute_id and not Attribute.query.get(attribute_id):
        return jsonify(message='Attribute ID is invalid or does not exist'), 400

    observation.name = data.get('name', observation.name)
    observation.description = data.get('description', observation.description)
    observation.attribute_id = data.get(
        'attribute_id', observation.attribute_id)
    db.session.commit()

    return jsonify({
        'observation_id': observation.observation_id,
        'name': observation.name,
        'description': observation.description,
        'attribute_id': observation.attribute_id
    }), 200


@observation_bp.route('/<int:observation_id>', methods=['DELETE'])
@token_required
@role_required('admin')
@swag_from({
    'tags': ['Observation'],
    'description': 'Delete a specific observation by its ID.',
    'parameters': [
        {
            'name': 'observation_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'The ID of the observation to delete'
        }
    ],
    'responses': {
        200: {
            'description': 'Observation deleted successfully'
        },
        404: {
            'description': 'Observation not found'
        }
    }
})
def delete_observation(current_user, observation_id: int):
    observation = Observation.query.get(observation_id)
    if observation:
        db.session.delete(observation)
        db.session.commit()
        return jsonify(message='Observation deleted'), 200
    else:
        return jsonify(message='Observation not found'), 404


@observation_bp.route('', methods=['GET'])
@token_required
@role_required('staff')
@swag_from({
    'tags': ['Observation'],
    'description': 'List all observations or search by attribute ID.',
    'parameters': [
        {
            'name': 'attribute_id',
            'in': 'query',
            'type': 'integer',
            'required': False,
            'description': 'The attribute ID to filter observations'
        }
    ],
    'responses': {
        200: {
            'description': 'List of observations retrieved successfully'
        }
    }
})
def list_observations(current_user):
    attribute_id = request.args.get('attribute_id')
    query = Observation.query
    if attribute_id:
        query = query.filter(Observation.attribute_id == attribute_id)
    observations = query.all()
    observations_data = [{
        'observation_id': obs.observation_id,
        'name': obs.name,
        'description': obs.description,
        'attribute_id': obs.attribute_id
    } for obs in observations]

    return jsonify(observations=observations_data), 200
