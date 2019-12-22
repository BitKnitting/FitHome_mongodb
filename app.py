#!/home/pi/projects/FitHome_mongodb/venv/bin/python3

# I went away from the more complex package style of
# Setting up a Flask environment as described in this
# YouTube video: https://youtu.be/3ZS7LEH_XBg?t=290

from flask import Flask
from flask import request
from datetime import datetime

from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/FitHome"
mongo = PyMongo(app)


# If an incoming reading comes in from the aggregate monitor,
# put it into the mongo db.
@app.route('/monitor', methods=['POST'])
def monitor():
    if request.is_json:
        req = request.get_json()
        try:
            now = datetime.now()
            timestamp_str = str(datetime.timestamp(now))
            # readings are going into the aggregate collection.
            monitor_collection = mongo.db.aggregate
            # Right now hard coded to microwave...will expand as learn more...
            # E.g.: Reading came in from monitor.
            reading = {"timestamp": timestamp_str,
                       "Pa": req['Pa'], "Pr": req['Pr'], }
            monitor_collection.insert(reading)
        except KeyError as error:
            print(f'The key {error} does not exist.', 400)
            return (f'The key {error} does not exist.', 400)
        except Exception as error:
            print(f'An error occurred: {error}', 400)
            return (f'An error occurred: {error}', 400)

        return 'Added a Reading!', 200
    else:
        return "Request was not JSON", 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4001, debug=True)
