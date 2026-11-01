from flask_restful import Resource
from flask_rest_service import api, mongo

# ----- / returns status OK and the MongoDB instance if the API is running -----
class Root(Resource):

    # ----- GET Request -----
    def get(self):
        return {
            'status': 'OK',
            'mongo': str(mongo.db),
        }


api.add_resource(Root, '/')