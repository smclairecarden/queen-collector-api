from flask import Blueprint, jsonify, request
from api.middleware import login_required, read_token

from api.models.db import db
from api.models.queen import Queen
from api.models.read import Read
from api.models.show import Show
from api.models.show import Association

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
  shows = Show.query.filter(Show.id.notin_([show.id for show in queen.shows])).all()
  shows=[show.serialize() for show in shows]
  return jsonify(queen=queen_data, available_shows=shows), 200

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


@queens.route('/<queen_id>/shows/<show_id>', methods=["LINK"]) 
@login_required
def assoc_toy(queen_id, show_id):
  data = { "queen_id": queen_id, "show_id": show_id }

  profile = read_token(request)
  queen = Queen.query.filter_by(id=queen_id).first()

  assoc = Association(**data)
  db.session.add(assoc)
  db.session.commit()

  queen = Queen.query.filter_by(id=queen_id).first()
  return jsonify(queen.serialize()), 201

@queens.errorhandler(Exception)          
def basic_error(err):
  return jsonify(err=str(err)), 500