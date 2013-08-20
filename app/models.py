from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Record(db.Model):
  __tablename__ = 'records'
  id = db.Column(db.Integer, primary_key=True)
  assignee = db.Column(db.String(100))
  date = db.Column(db.DateTime(timezone=True))
  suggested_value = db.Column(db.Float(asdecimal=True))
  reason = db.Column(db.String(1000))
  pledge_id = db.Column(db.Integer)
  reviewed = db.Column(db.Boolean)
  approved = db.Column(db.Boolean)
  value = db.Column(db.Float(asdecimal=True))

  def __init__(self, assignee, date, suggested_value, reason, pledge_id, reviewed=False, approved=False, value=None):
    self.assignee = assignee
    self.date = date
    self.suggested_value = suggested_value
    self.reason = reason
    self.pledge_id = pledge_id
    self.reviewed = reviewed
    self.approved = approved
    self.value = value

  @classmethod
  def get_all_records(cls):
    """
    Retrieves all records from the Records database for display on the front-end.
    """
    return db.session.query(Record).all()


class Pledge(db.Model):
  __tablename__ = 'pledges'
  id = db.Column(db.Integer, primary_key=True, unique=True)
  name = db.Column(db.String(100))
  major = db.Column(db.String(100))
  hometown = db.Column(db.String(100))

  def __init__(self, name, major, hometown):
    self.name = name
    self.major = major
    self.hometown = hometown

  
