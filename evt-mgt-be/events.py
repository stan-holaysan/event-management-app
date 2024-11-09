from flask import Blueprint, request, jsonify
from models import db, Event, User
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_cors import CORS, cross_origin

events_bp = Blueprint('events', __name__)
CORS(events_bp)

@events_bp.route('/', methods=['GET', 'OPTIONS'])
@cross_origin()
@jwt_required()
def get_events():
    events = Event.query.all()
    events_data = [{"id": e.id, "name": e.name, "description": e.description, "capacity": e.capacity, "booked": e.booked} for e in events]
    return jsonify(events_data)

@events_bp.route('/create', methods=['POST'])
@cross_origin()
@jwt_required()
def create_event():
    current_user = get_jwt_identity()
    data = request.get_json()
    event = Event(
        name=data['name'],
        description=data['description'],
        capacity=data['capacity'],
        booked=0,
        organizer_id=current_user['user_id']
    )
    db.session.add(event)
    db.session.commit()
    return jsonify(message="Event created successfully"), 201

@events_bp.route('/<int:event_id>', methods=['PUT'])
@cross_origin()
@jwt_required()
def edit_event(event_id):
    current_user = get_jwt_identity()
    event = Event.query.get_or_404(event_id)

    # Ensure only the event organizer or admin can edit
    if current_user['role'] not in ['admin', 'organizer'] or (current_user['role'] == 'organizer' and event.organizer_id != current_user['user_id']):
        return jsonify(message="Permission denied"), 403

    data = request.get_json()
    event.name = data.get('name', event.name)
    event.description = data.get('description', event.description)
    db.session.commit()
    return jsonify(message="Event updated successfully")

@events_bp.route('/increment/<int:event_id>', methods=['PUT'])
@cross_origin()
@jwt_required()
def increment(event_id):
    current_user = get_jwt_identity()
    event = Event.query.get_or_404(event_id)

    # Ensure only the event organizer or admin can edit
    if current_user['role'] not in ['admin', 'audience']:
        return jsonify(message="Permission denied"), 403

    # Check if the event can accommodate more attendees
    if event.booked >= event.capacity:
        return jsonify(message="Event is fully booked"), 400
    
    data = request.get_json()
    event.booked += 1
    db.session.commit()
    return jsonify(message="You have successfully booked a reservation")

@events_bp.route('/decrement/<int:event_id>', methods=['PUT'])
@cross_origin()
@jwt_required()
def decrement(event_id):
    current_user = get_jwt_identity()
    event = Event.query.get_or_404(event_id)

    # Ensure only the event organizer or admin can edit
    if current_user['role'] not in ['admin', 'audience']:
        return jsonify(message="Permission denied"), 403

    # Check if the event can accommodate more attendees
    if event.booked == 0:
        return jsonify(message="There are no reservations to cancel"), 400
    
    data = request.get_json()
    event.booked -= 1
    db.session.commit()
    return jsonify(message="The booking was cancelled")

@events_bp.route('/<int:event_id>', methods=['DELETE'])
@jwt_required()
def delete_event(event_id):
    current_user = get_jwt_identity()
    event = Event.query.get_or_404(event_id)

    # Ensure only the event organizer or admin can delete
    if current_user['role'] not in ['admin', 'organizer'] or (current_user['role'] == 'organizer' and event.organizer_id != current_user['user_id']):
        return jsonify(message="Permission denied"), 403

    db.session.delete(event)
    db.session.commit()
    return jsonify(message="Event deleted successfully")
