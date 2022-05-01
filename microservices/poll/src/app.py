from flask import request, Flask

from src.validators import validate_schema
from src.schemas import pool_schema, increment_schema
from src import repository

from bson.json_util import dumps


app = Flask(__name__)
BASE_PATH = '/api/polls'


@app.route("/", methods=['GET'])
def readyness():
    return "Ready"


@app.route(BASE_PATH, methods=['POST'])
@validate_schema(schema=pool_schema)
def post():
    result = repository.create_poll(request.get_json())
    return {"id": str(result.inserted_id)}, 201


@app.route(BASE_PATH, methods=['GET'])
def get_all():
    polls = list(repository.get_all_polls())
    for doc in polls:
        doc['id'] = str(doc['_id'])
        del doc['_id']
    return dumps(polls)


@app.route(f"{BASE_PATH}/<id>", methods=['GET'])
def get(id):
    poll = repository.find_poll(id)
    poll['id'] = str(poll['_id'])
    del poll['_id']
    return poll


@app.route(f"{BASE_PATH}/inc", methods=['PATCH'])
@validate_schema(schema=increment_schema)
def increment():
    id = request.get_json()['id']
    repository.increment_votes(id)
    return ''

# TODO: implement
# @app.route(f"{BASE_PATH}/val", methods=['POST'])
# @validate_schema(schema=increment_schema)
# def validate():
#     val_json = request.get_json()
#     id = val_json['id']
#     option = val_json['option']
#     repository.increment_votes(id)
#     return ''


def create_app():
    return app
