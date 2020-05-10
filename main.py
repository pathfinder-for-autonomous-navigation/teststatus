from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import datetime
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

statuses = ["Failing", "Unknown", "Passing"]
class TestData(db.Model):
    date = db.Column(db.DateTime, primary_key=True, default=datetime.datetime.utcnow)
    commit = db.Column(db.String(64), nullable=False)
    test =  db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(10), nullable=False)
    reporter = db.Column(db.String(10), nullable=False)

with open("tests.json") as f:
    tests = json.load(f)

@app.route('/reset')
def reset():
    """
    Resets tables in database
    """

    db.drop_all()
    db.create_all()
    return "Database has been reset"

@app.route('/dummy')
def create_test_data():
    """
    Endpoint used to create test data. Resets the database first.
    """

    db.drop_all()
    db.create_all()
    db.session.add(TestData(commit="bd5ff7328c0957ab0675e2de55c59cfd6839deaf", test="Teensy Unit Tests", status="Failing", reporter="Tanishq Aggarwal"))
    db.session.add(TestData(commit="abcdefg", test="HOOTL", status="Failing", reporter="Tanishq Aggarwal"))
    db.session.commit()
    return "Created test data"

@app.route('/')
def main():
    """
    Display view for testing status.
    """

    data_query = TestData.query.order_by(TestData.date.desc()).all()

    # Processes the database's data into something easily interpretable by the Jinja template
    # Is of the form:
    #
    # {
    #   "tests" : ["Teensy Unit Tests", "EmptyCase"],
    #   "commits" : {
    #       "bd5ff7328c0957ab0675e2de55c59cfd6839deaf" : {"test_data" : {"Teensy Unit Tests" : {"status" : "Failing", "reporter" : "Tanishq"}}}
    #   }
    # }

    data = {'commits' : {}, 'tests' : tests}
    for row in data_query:
        if not row.commit in data["commits"] : data["commits"][row.commit] = {"test_data" : {}}
        data["commits"][row.commit]["test_data"][row.test] = {"status" : row.status, "reporter" : row.reporter}

    return render_template("status.html", data=data, statuses=statuses)

@app.route('/change-status', methods=["POST"])
def change_status():
    """
    Endpoint used by UI to change the status of a test.
    """

    new_status = request.form["newStatus"]
    reporter = request.form["reporter"]
    commit = request.form["hash"]
    test = request.form["test"]

    test_data = TestData.query.filter_by(test=test,commit=commit).first()
    if test_data is None: return "not found"

    test_data.status = new_status
    test_data.reporter = reporter
    db.session.add(test_data)
    db.session.commit()
    return "changed"

@app.route('/new-commit', methods=["POST"])
def new_commit():
    """
    Endpoint used by Github webhook to add a new commit hash to the system.
    """

    if request.json["ref"] != "refs/heads/master": return "rejected"

    commits = [commit["id"] for commit in request.json["commits"]]
    for commit in commits:
        for test in tests:
            db.session.add(TestData(commit=commit,test=test,status="Unknown",reporter="Github"))
    db.session.commit()
    return "accepted"

if __name__ == "__main__":
    app.run(port=8000,ssl_context='adhoc')
