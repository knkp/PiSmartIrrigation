import sys, json
from datetime import datetime
from flask import Flask
from flask import send_from_directory
from flask import render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_url_path='')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pi_smart_irrigation.db'
db = SQLAlchemy(app)

# Models (put in another file shortly)
class SensorData(db.Model):
    data_id = db.Column(db.Integer, primary_key=True)
    measured_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    sensor_data = db.Column(db.Float, nullable=False)
    sensor_id = db.Column(db.Integer, db.ForeignKey('sensor.sensor_id'), nullable=False)
    sensor = db.relationship('Sensor', 
                backref=db.backref('sensor_data'))
    def __repr__(self):
        return '<val: %r>' % self.sensor_data


class Sensor(db.Model):
    sensor_id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(80), unique=True, nullable=False)
    sensor_type = db.Column(db.String(80), unique=True, nullable=False)
    # xLabels foreign key to SensorDataTable
    # sensor_data foreign key to SensorDataTable
    def __repr__(self):
        return '<type: %r>' % self.label



@app.route('/')
@app.route('/<path>')
def return_angular(path=None):
    if path == None:
        return send_from_directory('ng-app', 'index.html')
    else:
        return send_from_directory('ng-app', path)

@app.route('/api/sensors/list')
def get_sensor_list():
    return json.dumps(
        {
            "Humidity": {
                "list": [
                    {
                        "id": 1,
                        "name": "Humidity 1"
                    }
                ]
            }
        }
    )

@app.route('/api/sensors/<id>')
def get_sensor_details(id=None):
    return json.dumps({ 
            "id": 1, 
            "data": [1, 2, 3, 4, 5, 6], 
            "label": "Humidity 1", 
            "type": "humidity",
            "xLabels": ['1', '2', '3', '4', '5', '6']
    })

if __name__ == "__main__":
    app.run()

