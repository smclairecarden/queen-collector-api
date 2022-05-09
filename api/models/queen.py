from datetime import datetime
from api.models.db import db

class Queen(db.Model):
    __tablename__ = 'queens'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    season = db.Column(db.Integer)
    description = db.Column(db.String(250))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    profile_id = db.Column(db.Integer, db.ForeignKey('profiles.id'))

    reads = db.relationship("Read", cascade='all')

    def __repr__(self):
      return f"Queen('{self.id}', '{self.name}'"

    def serialize(self):
      queen = {c.name: getattr(self, c.name) for c in self.__table__.columns}
      reads = [read.serialize() for read in self.reads] 
      queen['reads'] = reads
      return queen