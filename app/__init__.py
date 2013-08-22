import datetime
import json

from flask import Flask, jsonify, render_template, request

from models import db, Record, Pledge, pledge_id_to_name

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:padres100@localhost:3306/merits'
db.init_app(app)


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
  pledge_name = request.form['pledgeName'] 
  suggested_value = request.form['suggestedValue']
  now = datetime.date.today() 

  pledge_id = Pledge.get_pledge_by_name(pledge_name).id

  record_id = Record.add_record(name, now, suggested_value, justification, pledge_id)
  return 'Request Successfully Submited' 


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

  pledge_id = Pledge.get_pledge_by_name(pledge).id
  records = Record.get_records_by_pledge(pledge_id)     

  approved = [r for r in records if r.approved]
  pending = [r for r in records if not r.reviewed]
  rejected = [r for r in records if r.reviewed and not r.approved]
  return render_template('pledge.html', page_title=title, approved=approved, pending=pending, rejected=rejected)


@app.route('/summary')
def get_merit_summary():
  """
  Render the summary page.
  """
  title = 'Summary'
  return render_template('summary.html', page_title=title)


@app.route('/review')
def render_review_page():
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
  approved = json.loads((request.form['approved']))
  for request_id in approved:
    value = float(approved[request_id])
    Record.approve_request(int(request_id), value)

  rejected = request.form['rejected'].split(',')
  for request_id in rejected:
    if request_id:
      Record.reject_request(request_id)

  return jsonify(success=1)

@app.route('/test')
def test():
  0/0
