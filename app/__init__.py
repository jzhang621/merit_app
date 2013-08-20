from flask import Flask, render_template
from models import db, Record

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:padres100@localhost:3306/merits'
app.config['SQLALCHEMY_ECHO'] = True

db.init_app(app)

@app.route('/testdb')
def testdb():
  if db.session.query('1').from_statement('Select 1').all():
    return 'It works.'
  else:
    return 'Something is broken.'

@app.route('/')
def get_all_records():
  """
  Returns all merits in the database for viewing.
  """
  return render_template('layout.html')
