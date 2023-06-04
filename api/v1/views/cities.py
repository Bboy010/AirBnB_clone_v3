#!/usr/bin/python3
"""View for City objects
"""


from flask import Flask, jsonify, request, abort
from models import storage
from models.state import State, City
from api.v1.views import app_views


@app_views.route('/states/<state_id>/cities', methods=['GET'])
def get_cities_of_state(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    cities_list = [city.to_dict() for city in state.cities]
    return jsonify(cities_list)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route('states/<state_id>/cities', methods=['POST'])
def create_city(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'name' not in request.get_json():
        abort(400, 'Missing name')
    city = City(**request.get_json())
    city.save()
    state.cities.append(city)
    return jsonify(city.to_dict()), 201


@app_views.route('cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    data = request.get_json()
    ignore_keys = ['id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(city, key, value)
    city.save()
    return jsonify(city.to_dict()), 200
