import json
import pymongo
from flask import request, abort, json, Flask, render_template
from flask.ext import restful
from flask.ext.restful import reqparse
from flask_rest_service import app, api, mongo
from bson.objectid import ObjectId
from bson.code import Code

# ----- / returns status OK and the MongoDB instance if the API is running -----
class Root(restful.Resource):

    # ----- GET Request -----
    def get(self):
        return {
            'status': 'OK',
            'mongo': str(mongo.db),
        }


api.add_resource(Root, '/')