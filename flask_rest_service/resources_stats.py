import json
import pymongo
from flask import request, abort, json, render_template, make_response
from flask.ext import restful
from flask.ext.restful import reqparse
from flask_rest_service import app, api, mongo
from bson.objectid import ObjectId
from bson.code import Code

# ----- / returns stats index -----
class StatsIndex(restful.Resource):

    # ----- GET Request -----
	def get(self):
		response = make_response(render_template('index_stats.html'))
		response.headers['content-type'] = 'text/html'
		return response


api.add_resource(StatsIndex, '/stats')