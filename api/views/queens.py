from flask import Blueprint, jsonify, request
from api.middleware import login_required, read_token

from api.models.db import db
from api.models.queen import Queen
from api.models.read import Read


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

@queens.route('/<id>', methods=["PUT"]) 
@login_required
def update(id):
  data = request.get_json()
  profile = read_token(request)
  queen = Queen.query.filter_by(id=id).first()

  if queen.profile_id != profile["id"]:
    return 'Forbidden', 403

  for key in data:
    setattr(queen, key, data[key])

  db.session.commit()
  return jsonify(queen.serialize()), 200

@queens.route('/<id>', methods=["DELETE"]) 
@login_required
def delete(id):
  profile = read_token(request)
  queen = Queen.query.filter_by(id=id).first()

  if queen.profile_id != profile["id"]:
    return 'Forbidden', 403

  db.session.delete(queen)
  db.session.commit()
  return jsonify(message="Success"), 200

@queens.route('/<id>/reads', methods=["POST"]) 
@login_required
def add_feeding(id):
  data = request.get_json()
  data["queen_id"] = id

  profile = read_token(request)
  queen = Queen.query.filter_by(id=id).first()

  read = Read(**data)
  
  db.session.add(read)
  db.session.commit()

  queen_data = queen.serialize()

  return jsonify(queen_data), 201