from flask import Blueprint
from flask import request

from .extensions import mongo
from datetime import datetime

main = Blueprint('main', __name__)

MICROWAVE_ON = 0
@main.route('/')
def index():
    now = datetime.now()
#
# The Microwave PlugE device is sending the state of the microwave
#
@main.route('/microwave', methods=['POST'])
def microwave():
    global MICROWAVE_ON
    if request.is_json:
        req = request.get_json()
        try:
            MICROWAVE_ON = req['device_on']
            print('microwave is: {}'.format(MICROWAVE_ON))
            return 'Added microwave info!', 200
        except KeyError as error:
            print(f'The key {error} does not exist.', 400)
            return (f'The key {error} does not exist.', 400)
    else:
        return "Request was not JSON", 400
#
# Add a monitor reading to the db
# The reading goes into the aggregated collection.
# So far, we have added training on a microwave.
#
@main.route('/monitor', methods=['POST'])
def monitor():
    global MICROWAVE_ON
    if request.is_json:
        req = request.get_json()
        try:
            now = datetime.now()
            timestamp_str = str(datetime.timestamp(now))
            # readings are going into the aggregated collection.
            monitor_collection = mongo.db.aggregated
            # Right now hard coded to microwave...will expand as learn more...
            # E.g.: Reading came in from monitor.
            reading = {"timestamp": timestamp_str,
                       "Pa": req['Pa'], "I": req['I'], "Pr": req['Pr'], "microwave": MICROWAVE_ON, }
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
