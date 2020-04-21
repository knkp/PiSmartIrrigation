import sys, json, random
from datetime import datetime
from flask import Flask
from flask import send_from_directory
from flask import render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import asc

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
    label = db.Column(db.String(80), nullable=False)
    sensor_type = db.Column(db.String(80), nullable=False)
    # xLabels foreign key to SensorDataTable
    # sensor_data foreign key to SensorDataTable
    def __repr__(self):
        return '<type: %r>' % self.label


def make_db(add_test_data=False):
    db.drop_all()
    db.create_all()
    if add_test_data:    
        # add some default sensors and random sensor data
        sensor1 = Sensor(label='Humidity 1', sensor_type='humidity')
        sensor2 = Sensor(label='Humidity 2', sensor_type='humidity')
        data_count = 10
        i = 0
        while i < data_count:
            data = SensorData(sensor_data = random.random()*100)
            sensor1.sensor_data.append(data)
            i += 1
        
        i = 0
        while i < data_count:
            data = SensorData(sensor_data = random.random()*100)
            sensor2.sensor_data.append(data)
            i += 1
        db.session.add(sensor1)
        db.session.add(sensor2)
        db.session.commit()
        


# generate list of sensors for response
def return_sensor_list():
    json_sensors = {}
    query = db.session.query(Sensor.sensor_type.distinct().label("sensor_type"))
    sensor_types = [row.sensor_type for row in query.all()]
    for stype in sensor_types:
        json_sensors[stype] = dict() 
        json_sensors[stype]["list"] = list()
        sensors_result = Sensor.query.filter_by(sensor_type=stype).order_by(asc(Sensor.sensor_id))
        for result in sensors_result:
            sensor_item = dict()
            sensor_item["id"] = result.sensor_id
            sensor_item["name"] = result.label
            json_sensors[stype]["list"].append(sensor_item)
    return json_sensors

def return_sensor_id_data(id):
    # query the data
    sensor = Sensor.query.filter_by(sensor_id=id).first()
    this_data = SensorData.query.with_parent(sensor).order_by(SensorData.measured_time.desc()).limit(10)
    # assemble results 
    response = dict()
    response["id"] = sensor.sensor_id
    response["label"] = sensor.label
    response["type"] = sensor.sensor_type

    # collect data and labels
    data_itself = list()
    xLabels = list()
    for item in this_data:
        data_itself.insert(0,item.sensor_data)
        xLabels.insert(0,item.measured_time)
    response["data"] =  data_itself
    response["xLabels"] = xLabels

    return response

@app.route('/')
@app.route('/<path>')
def return_angular(path=None):
    if path == None:
        return send_from_directory('ng-app', 'index.html')
    else:
        return send_from_directory('ng-app', path)

@app.route('/api/sensors/list')
def get_sensor_list():
    slist = return_sensor_list()
    return json.dumps(slist)

@app.route('/api/sensors/<id>')
def get_sensor_details(id=None):
    response = return_sensor_id_data(id)
    return response
    

if __name__ == "__main__":
    app.run()

