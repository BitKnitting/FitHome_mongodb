
from flask import Blueprint
from flask import request

from .extensions import mongo
from datetime import datetime

main = Blueprint('main', __name__)

# A FitHome Monitor sends a post to this service with a reading.
#
# Add a monitor reading to the db
# The reading goes into the aggregated collection.
#
@main.route('/monitor', methods=['POST'])
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
