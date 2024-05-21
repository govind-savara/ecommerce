import json
from bson import json_util


def parse_mongo_json(data):
    """ Parse mongodb collection elements data with _id to json data"""
    return json.loads(json_util.dumps(data))