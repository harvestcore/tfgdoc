from flask import request
from flask_restplus import Resource, Namespace

from src.classes.docker_engine import DockerEngine
from src.classes.login import Login
from src.classes.mongo_engine import MongoEngine
from src.classes.user import User
from src.services.login import token_required
from src.utils.response_by_success import response_by_success


api = Namespace(name='status', description='Status')


@api.route('')
class StatusService(Resource):

    @staticmethod
    @token_required
    def get():
        user = Login().get_username(request.headers['x-access-token'])

        if user and User().is_admin(user):
            return {
                'mongo': MongoEngine().status(),
                'docker': DockerEngine().status()
            }, 200
        return response_by_success(False)
