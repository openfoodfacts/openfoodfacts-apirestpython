from flask import render_template, Response
import flask_restful as restful
from flask_rest_service import api


# ----- /stats -----
class Stats(restful.Resource):

    # ----- GET Request -----
    def get(self):
        return Response(render_template("index.html") , mimetype='text/html')



api.add_resource(Stats, '/stats')