from flask import Flask, request
from dotenv import load_dotenv

from src import microservices, repository
from src.validators import validate_schema
from src.schemas import vote_schema


load_dotenv()

app = Flask(__name__)
BASE_PATH = "/api/votes"


@app.route("/", methods=['GET'])
def readiness():
    return "Ready", 200


@validate_schema(schema=vote_schema)
@app.route(BASE_PATH, methods=['POST'])
def post():
    vote_json = request.get_json()
    repository.vote(vote_json)
    microservices.increment_pool(vote_json['pool_id'])
    return "", 201


def create_app():
    return app
