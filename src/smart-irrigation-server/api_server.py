import sys, json
from flask import Flask
from flask import send_from_directory
from flask import render_template, request
app = Flask(__name__, static_url_path='')

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
            "type": "humidity" 
    })

if __name__ == "__main__":
    app.run()

