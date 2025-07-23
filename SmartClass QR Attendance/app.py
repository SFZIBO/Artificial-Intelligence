from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import base64
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///attendance.db'
db = SQLAlchemy(app)

class AttendanceSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer)
    session_date = db.Column(db.Date)
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)
    qr_token = db.Column(db.String(255), unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class AttendanceRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer)
    student_id = db.Column(db.Integer)
    scan_time = db.Column(db.DateTime)
    status = db.Column(db.String(20))
    location = db.Column(db.String(100))

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/scan')
def scan():
    return render_template('scan.html')

@app.route('/submit_scan', methods=['POST'])
def submit_scan():
    data = request.get_json()
    token = data['qr_token']
    student_id = data['student_id']
    location = data['location']
    now = datetime.now()

    session = AttendanceSession.query.filter_by(qr_token=token).first()
    if not session:
        return jsonify({"status": "invalid", "reason": "QR not recognized"})

    start = datetime.combine(session.session_date, session.start_time)
    end = datetime.combine(session.session_date, session.end_time)
    status = "ontime" if start <= now <= end else "late"

    record = AttendanceRecord(
        session_id=session.id,
        student_id=student_id,
        scan_time=now,
        status=status,
        location=location
    )
    db.session.add(record)
    db.session.commit()
    return jsonify({"status": status, "scan_time": now.isoformat()})

if __name__ == '__main__':
    with app.app_context():
        if not os.path.exists('attendance.db'):
            db.create_all()
    app.run(debug=True)

