from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Record(db.Model):
  __tablename__ = 'records'
  id = db.Column(db.Integer, primary_key=True)
  assignee = db.Column(db.String(100))
  date = db.Column(db.Date)
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

  @classmethod
  def get_all_pending_records(cls):
    """
    Returns all the requests that are pending approval
    """
    return db.session.query(Record).filter(Record.reviewed == False).all()

  @classmethod
  def approve_request(cls, request_id, new_value):
    """
    Approves an entry in the records table with the new value.
    """
    # first modify the reviewed, approved, and value fields
    record = db.session.query(Record) \
              .filter(Record.id == request_id) \
              .first()

    record.reviewed = True
    record.approved = True
    record.value = new_value

    pledge = db.session.query(Pledge) \
               .filter(Pledge.id == record.pledge_id) \
               .first()

    pledge.value += new_value

    db.session.commit()
    return record.id
 
  @classmethod
  def reject_request(cls, request_id):
    """
    Rejects an entry in the records table by setting approved to false and reviewed to true.
    """
    record = db.session.query(Record) \
              .filter(Record.id == request_id) \
              .first()

    record.reviewed = True
    record.approved = False
  
    db.session.commit()
    return record.id

class Pledge(db.Model):
  __tablename__ = 'pledges'
  id = db.Column(db.Integer, primary_key=True, unique=True)
  name = db.Column(db.String(100))
  major = db.Column(db.String(100))
  year = db.Column(db.String(10))
  value = db.Column(db.Float())

  def __init__(self, name, major, year, value=0):
    self.name = name
    self.major = major
    self.year = year
    self.value = value

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

  #TODO Cache this method
  @classmethod
  def get_all_pledges(cls):
    """
    Returns all pledges currently registered in the pledges database.
    """
    return db.session.query(Pledge).order_by(Pledge.id).all()


# TODO Cache this method
def pledge_id_to_name():
  """
  Returns a dictionary mapping pledge_id's to pledge names
  """
  pledge_map = {}
  pledges = Pledge.get_all_pledges()
  
  for p in pledges:
    pledge_map[p.id] = p.name

  return pledge_map

