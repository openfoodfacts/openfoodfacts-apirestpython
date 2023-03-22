import json
import pymongo
from flask import request, abort, json, render_template, Response
import flask_restful as restful
from flask_rest_service import app, api, mongo
from bson.objectid import ObjectId
from bson.code import Code


# ----- /stats -----
class Stats(restful.Resource):

    # ----- GET Request -----
    def get(self):
        return Response(render_template("index.html") , mimetype='text/html')



api.add_resource(Stats, '/stats')