import datetime
import fetch
import flask
import json
app = flask.Flask(__name__)

@app.route('/')
def full_schedule():
    schedule = fetch.schedule()
    resp = flask.make_response(json.dumps(schedule))
    resp.status='200'
    resp.mimetype="application/json"
    return resp

@app.route('/today')
def today():
    schedule = fetch.schedule()
    today = datetime.date.today().isoformat()
    my_item = [item for item in schedule if item.get('date') == today]
    resp = flask.make_response(json.dumps(my_item))
    resp.status='200'
    resp.mimetype="application/json"
    return resp

@app.route('/tomorrow')
def tomorrow():
    schedule = fetch.schedule()
    tomorrow = (datetime.date.today() + datetime.timedelta(days=1)).isoformat()
    my_item = [item for item in schedule if item.get('date') == tomorrow]
    resp = flask.make_response(json.dumps(my_item))
    resp.status='200'
    resp.mimetype="application/json"
    return resp

if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)
