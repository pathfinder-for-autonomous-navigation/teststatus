from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)

statuses = ["Failing", "Unknown", "Passing"]
class TestData(db.Model):
    name =  db.Column(db.String(255))
    status = db.Column(db.String(10))
    reporter = db.Column(db.String(10))

class CommitData(db.Model):
    commit = db.Column(db.String(64))
    test_data = db.relationship('TestData')

data = {
    "tests" : ["Teensy Unit Tests", "EmptyCase"],
    "commits" : {
        #"bd5ff7328c0957ab0675e2de55c59cfd6839deaf" : {"test_data" : {"Teensy Unit Tests" : {"status" : "Failing", "reporter" : "Tanishq"}}}
    }
}

@app.route('/')
def hitl():
    CommitData.query.filter_by()

    return render_template("status.html", data=data, statuses=statuses)

@app.route('/change-status', methods=["POST"])
def change_status():
    new_status = request.form["newStatus"]
    reporter = request.form["reporter"]
    commit = request.form["hash"]
    test = request.form["test"]

    data["commits"][commit]["test_data"][test]["status"] = new_status
    data["commits"][commit]["test_data"][test]["reporter"] = reporter

    return ""

if __name__ == "__main__":
    app.run(port=8080)
