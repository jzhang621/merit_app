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
  def add_record(cls, assignee, date, suggested_value, reason, pledge_id):
    """
    Creates a new record object with the given parameters and commits to the database.
    """
    new_record = Record(assignee, date, suggested_value, reason, pledge_id)
    db.session.add(new_record) 
    db.session.commit() 
    return new_record.id
  
  @classmethod
  def get_all_records(cls):
    """
    Retrieves all records from the Records database for display on the front-end.
    """
    return db.session.query(Record).all()

  @classmethod
  def get_records_by_pledge(cls, pledge_id):
    """
    Returns all the merits or demerits assigned to the given pledge.
    """
    return db.session.query(Record).filter(Record.pledge_id == pledge_id).all()


class Pledge(db.Model):
  __tablename__ = 'pledges'
  id = db.Column(db.Integer, primary_key=True, unique=True)
  name = db.Column(db.String(100))
  major = db.Column(db.String(100))
  year = db.Column(db.String(10))

  def __init__(self, name, major, year):
    self.name = name
    self.major = major
    self.year = year

  @classmethod
  def add_pledge(cls, name, major, year):
    """
    Creates a new pledge object given the parameters and commits to the database.
    """
    new_pledge = Pledge(name, major, year)
    db.session.add(new_pledge)
    db.session.commit()
    return new_pledge.id

  @classmethod
  def get_pledge_by_name(cls, name):
    """
    Given a pledge name, return the associated pledge object.
    """
    return db.session.query(Pledge).filter(Pledge.name == name).first()

  @classmethod
  def get_all_pledges(cls):
    """
    Returns all pledges currently registered in the pledges database.
    """
    return db.session.query(Pledge).all()
