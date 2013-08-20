from flask import Flask, render_template
from models import db, Record

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:padres100@localhost:3306/merits'
app.config['SQLALCHEMY_ECHO'] = True

db.init_app(app)


@app.context_processor
def register_pledges():
  pledges = ['Albert', 'Amy', 'Andre', 'Betty', 'Chris', 'Daniel', 'Gabe', 'Julia', 'Kai', 'Ling', 'Matt', 'Nicole']
  return dict(pledges=pledges)


### ---- ROUTES ---- ###

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

@app.route('/new')
def new_request():
  """
  Renders the HTML page for a new merit request
  """
  return render_template('new_request.html')
