import json
import pymongo
from flask import request, abort, json
from flask.ext import restful
from flask.ext.restful import reqparse
from flask_rest_service import app, api, mongo
from bson.objectid import ObjectId
from bson.code import Code

# ----- /products -----
class ProductsList(restful.Resource):

    # ----- GET Request -----
    def get(self):
        # ----- Get limit # in the request, 50 by default -----
        limit = request.args.get('limit',default=50,type=int)
        # ----- Get skip # in the request, 0 by default -----
        skip = request.args.get('skip',default=0,type=int)
        # ----- Get count # in the request, 0 by default -----
        count = request.args.get('count',default=0, type=int)
        # ----- See if we want short response or not, 0 by default -----
        short = request.args.get('short',default=0, type=int)
        # ----- Query -----
        query = request.args.get('q')


        # ----- The regex param makes it search "like" things, the options one tells to be case insensitive
        data = dict((key, {'$regex' : request.args.get(key), '$options' : '-i'}) for key in request.args.keys())

        # ----- Delete custom parameters from the request, since they are not in MongoDB -----
        # ----- And add filters to custom parameters : -----
        if request.args.get('limit'):
            del data['limit']

        if request.args.get('skip'):
            del data['skip']

        if request.args.get('count'):
            del data['count']

        if request.args.get('short'):
            del data['short']

        if request.args.get('q'):
            del data['q']

        # ----- Filter data returned -----
        # ----- If we just want a short response -----
        # ----- Tell which fields we want -----
        fieldsNeeded = {'code':1, 'lang':1, 'product_name':1}
        if request.args.get('short') and short == 1:
            if request.args.get('count') and count == 1 and not request.args.get('q'):
                return mongo.db.products.find(data, fieldsNeeded).sort('created_t', pymongo.DESCENDING).skip(skip).limit(limit).count()
            elif not request.args.get('count') and not request.args.get('q'):
                return mongo.db.products.find(data, fieldsNeeded).sort('created_t', pymongo.DESCENDING).skip(skip).limit(limit)
            elif request.args.get('count') and count == 1 and request.args.get('q'):
                return mongo.db.products.find({ "$text" : { "$search": query } }, fieldsNeeded).sort('created_t', pymongo.DESCENDING).skip(skip).limit(limit).count()
            else:
                return mongo.db.products.find({ "$text" : { "$search": query } }, fieldsNeeded).sort('created_t', pymongo.DESCENDING).skip(skip).limit(limit)
        else:
            if request.args.get('count') and count == 1 and not request.args.get('q'):
                return mongo.db.products.find(data).sort('created_t', pymongo.DESCENDING).skip(skip).limit(limit).count()
            elif not request.args.get('count') and not request.args.get('q'):
                return mongo.db.products.find(data).sort('created_t', pymongo.DESCENDING).skip(skip).limit(limit)
            elif request.args.get('count') and count == 1 and request.args.get('q'):
                return mongo.db.products.find({ "$text" : { "$search": query } }).sort('created_t', pymongo.DESCENDING).skip(skip).limit(limit).count()
            else:
                return mongo.db.products.find({ "$text" : { "$search": query } }).sort('created_t', pymongo.DESCENDING).skip(skip).limit(limit)
               

# ----- /product/<product_id> -----
class ProductId(restful.Resource):

    # ----- GET Request -----
    def get(self, barcode):
        return  mongo.db.products.find_one({"code":barcode})


# ----- /products/brands -----
class ProductsBrands(restful.Resource):

    # ----- GET Request -----
    def get(self):
        # ----- Get count # in the request, 0 by default -----
        count = request.args.get('count',default=0, type=int)
        query = request.args.get('query')

        if request.args.get('query'):
            map = Code("function () {"
                        "   if (!this.brands) return;"
                        "   emit(this.brands.trim(), 1);"
                        "};")

            reduce = Code("function (key, values) {"
                        "   var count = 0;"
                        "       for (index in values) {"
                        "           count += values[index];"
                        "       }"
                        "       return count;"    
                        "   };")

            result = mongo.db.products.map_reduce(map, reduce, "brands_products")

            res = []
            for doc in result.find({"_id": {'$regex' : query, '$options' : '-i'}}):
                res.append(doc['_id'])
            if request.args.get('count') and count == 1:
                return len(res)
            else:
                return res
        else:
            if request.args.get('count') and count == 1:
                return  len(mongo.db.products.distinct('brands'))
            else:
                return  mongo.db.products.distinct('brands')
            


# ----- / returns status OK and the MongoDB instance if the API is running -----
class Root(restful.Resource):

    # ----- GET Request -----
    def get(self):
        return {
            'status': 'OK',
            'mongo': str(mongo.db),
        }


api.add_resource(Root, '/')
api.add_resource(ProductsList, '/products')
api.add_resource(ProductsBrands, '/products/brands')
api.add_resource(ProductId, '/product/<string:barcode>')