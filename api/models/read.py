from datetime import datetime
from api.models.db import db

class Read(db.Model):
    __tablename__ = 'reads'
    id = db.Column(db.Integer, primary_key=True)
    read = db.Column(db.String(250))
    name = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.now(tz=None))
    queen_id = db.Column(db.Integer, db.ForeignKey('queens.id'))


    def __repr__(self):
      return f"Read('{self.id}', '{self.read}'"

    def serialize(self):
      read = {c.name: getattr(self, c.name) for c in self.__table__.columns}
      return read
