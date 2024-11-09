from flask import Blueprint, request, jsonify
from models import db, Reservation, Event
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_cors import CORS, cross_origin

reservations_bp = Blueprint('reservations', __name__)
CORS(reservations_bp)

@reservations_bp.route('/<int:event_id>', methods=['POST'])
@cross_origin()
@jwt_required()
def book_reservation(event_id):
    current_user = get_jwt_identity()
    event = Event.query.get_or_404(event_id)

    # Create a reservation
    reservation = Reservation(event_id=event.id, user_id=current_user['user_id'])
    db.session.add(reservation)
    db.session.commit()
    return jsonify(message="Reservation booked successfully")

@reservations_bp.route('/<int:event_id>', methods=['DELETE'])
@cross_origin()
@jwt_required()
def cancel_reservation(event_id):
    current_user = get_jwt_identity()
    reservation = Reservation.query.filter_by(event_id=event_id, user_id=current_user['user_id']).first_or_404()

    # Remove the reservation
    db.session.delete(reservation)
    db.session.commit()
    return jsonify(message="Reservation canceled successfully")
