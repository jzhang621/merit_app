import datetime
from functools import wraps
import json
import os

from flask import Flask, jsonify, render_template, redirect, request, url_for

from models import db, Record, Pledge, pledge_id_to_name

app = Flask(__name__)

if os.environ.get('DATABASE_URL') is None:
  app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:padres100@localhost:3306/merits'
else:
  # heroku configs
  app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']

db.init_app(app)
db.app = app
db.create_all()

@app.context_processor
def register_pledges():
  pledges = Pledge.get_all_pledges()
  return dict(pledges=pledges)

@app.template_filter('first_name')
def first_name_filter(s):
  return s.split(' ')[0]

@app.template_filter('convert_date')
def convert_date_filter(date):
  return str(date)

@app.template_filter('id_to_name')
def id_to_name(pledge_id):
  pledge_map = pledge_id_to_name()
  return pledge_map[pledge_id]

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        return redirect(url_for('render_login_page', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


### ---- VIEWS ---- ###

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
  pledges = request.form['pledges'].split(',')
  suggested_value = request.form['suggestedValue']
  now = datetime.date.today()

  for pledge_id in pledges:
    record_id = Record.add_record(name, now, suggested_value, justification, pledge_id)
  return 'Request Successfully Submited'


@login_required
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


@app.route('/report/<pledge>')
def get_pledge_report(pledge):
  """
  Render the merit report for the given pledge
  """
  title = pledge
  pledge_info = Pledge.get_pledge_by_name(pledge)

  pledge_id = pledge_info.id
  total = pledge_info.value
  records = Record.get_records_by_pledge(pledge_id)

  approved = [r for r in records if r.approved]
  pending = [r for r in records if not r.reviewed]
  rejected = [r for r in records if r.reviewed and not r.approved]
  return render_template('pledge.html', page_title=title, approved=approved, pending=pending, rejected=rejected, pledge_total=total)


@app.route('/summary')
def get_merit_summary():
  """
  Render the summary page.
  """
  title = 'Summary'
  return render_template('summary.html', page_title=title)


@app.route('/review')
@login_required
def render_review_page():
  """
  Render the review page.
  """
  title = 'Review'
  pending = Record.get_all_pending_records()
  return render_template('review.html', page_title=title, pending=pending)


@app.route('/approve_requests', methods=['POST'])
def approve_requests():
  """
  Approve or reject the requests as specified by request_id.

  1) Approved requests are mapped from a request_id to the approved value of the request.
  2) Rejected requests are identified by a request_id only.
  """
  processed = []
  approved = json.loads((request.form['approved']))
  for request_id in approved:
    value = float(approved[request_id])
    record_id = Record.approve_request(int(request_id), value)
    processed.append(record_id)

  rejected = request.form['rejected'].split(',')
  for request_id in rejected:
    if request_id:
      record_id = Record.reject_request(request_id)
      processed.append(record_id)

  return jsonify(success=processed)

@app.route('/login')
def render_login_page():
  title = 'Login'
  return render_template('login.html', page_title=title)

