from flask import Blueprint, jsonify, request
from api.middleware import login_required, read_token

from api.models.db import db
from api.models.queen import Queen

queens = Blueprint('queens', 'queens')

@queens.route('/', methods=["POST"])
@login_required
def create():
  data = request.get_json()
  profile = read_token(request)
  data["profile_id"] = profile["id"]
  queen = Queen(**data)
  db.session.add(queen)
  db.session.commit()
  return jsonify(queen.serialize()), 201

@queens.route('/', methods=["GET"])
def index():
  queens = Queen.query.all()
  return jsonify([queen.serialize() for queen in queens]), 200

@queens.route('/<id>', methods=["GET"])
def show(id):
  queen = Queen.query.filter_by(id=id).first()
  queen_data = queen.serialize()
  return jsonify(queen=queen_data), 200