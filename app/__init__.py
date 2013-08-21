from flask import Flask, render_template, request
from models import db, Record, Pledge
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:padres100@localhost:3306/merits'

db.init_app(app)


@app.context_processor
def register_pledges():
  pledges = ('Albert', 'Amy', 'Andre', 'Betty', 'Chris', 'Daniel', 'Gabe', 'Julia', 'Kai', 'Ling', 'Matt', 'Nicole')
  return dict(pledges=pledges)


### ---- ROUTES ---- ###

@app.route('/')
@app.route('/new_request')
def render_new_request_page():
  """
  Renders the HTML page for a new merit request
  """
  title = 'New Request'
  return render_template('new_request.html', page_title=title)


@app.route('/commit_request', methods=['POST'])
def commit_request():
  """
  API endpoint used by the front-end to commit a new merit request in ther records database
  """
  name = request.form['name']
  justification = request.form['justification']
  pledge_name = request.form['pledgeName'] 
  suggested_value = request.form['suggestedValue']

  return "<h1>success</h1>"


@app.route('/register_pledge')
def render_register_pledge_page():
  """
  Renders the HTML page to add a new pledge to the database
  """
  title = 'Register Pledge'
  return render_template('register_pledge.html', page_title=title)


@app.route('/commit_pledge', methods=['POST'])
def commit_pledge():
  """
  API endpoint used by the front-end to commit a pledge in the pledges database.
  """
  name = request.form['pledgeName']
  major = request.form['major']
  year = request.form['year']

  pledge_id = Pledge.add_pledge(name, major, year)
  return '<div>{0}</div>'.format(pledge_id)


@app.route('/<pledge>')
def get_pledge_report(pledge):
  """
  Render the merit report for the given pledge
  """
  pass


@app.route('/summary')
def get_merit_summary():
  title = 'Summary'
  return render_template('summary.html', page_title=title)

@app.route('/test')
def test():
  0/0
