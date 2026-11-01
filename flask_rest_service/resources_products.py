import pymongo
from flask import request
import flask_restful as restful
from flask_rest_service import api, mongo

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
                return mongo.db.products.count_documents(data)
            elif not request.args.get('count') and not request.args.get('q'):
                return mongo.db.products.find(data, fieldsNeeded).sort('created_t', pymongo.DESCENDING).skip(skip).limit(limit)
            elif request.args.get('count') and count == 1 and request.args.get('q'):
                return mongo.db.products.count_documents({ "$text" : { "$search": query } })
            else:
                return mongo.db.products.find({ "$text" : { "$search": query } }, fieldsNeeded).sort('created_t', pymongo.DESCENDING).skip(skip).limit(limit)
        else:
            if request.args.get('count') and count == 1 and not request.args.get('q'):
                return mongo.db.products.count_documents(data)
            elif not request.args.get('count') and not request.args.get('q'):
                return mongo.db.products.find(data).sort('created_t', pymongo.DESCENDING).skip(skip).limit(limit)
            elif request.args.get('count') and count == 1 and request.args.get('q'):
                return mongo.db.products.count_documents({ "$text" : { "$search": query } })
            else:
                return mongo.db.products.find({ "$text" : { "$search": query } }).sort('created_t', pymongo.DESCENDING).skip(skip).limit(limit)


# ----- /products/stats/info-----
class ProductsStats(restful.Resource):

    # ----- GET Request -----
    def get(self):

        # Aggregation replacement for the old map_reduce (removed in
        # PyMongo 4.0 and unsupported by MongoDB Server 5.0+).
        # Buckets products by creation year/month and nutrient levels.
        # Note: month is 1-based ($month); the old JS used 0-based
        # getMonth() and additionally skipped January docs via a falsy
        # check, which the dashboard's "%Y-%m" date parsing never
        # supported anyway.
        pipeline = [
            {"$match": {"created_t": {"$type": "number"}}},
            {"$project": {
                "date": {"$toDate": {"$multiply": ["$created_t", 1000]}},
                "saltlevels": {"$ifNull": ["$nutrient_levels.salt", None]},
                "fatlevels": {"$ifNull": ["$nutrient_levels.fat", None]},
                "saturatedfatlevels": {"$ifNull": ["$nutrient_levels.saturated-fat", None]},
                "sugarslevels": {"$ifNull": ["$nutrient_levels.sugars", None]},
            }},
            {"$group": {
                "_id": {
                    "year": {"$year": "$date"},
                    "month": {"$month": "$date"},
                    "saltlevels": "$saltlevels",
                    "fatlevels": "$fatlevels",
                    "saturatedfatlevels": "$saturatedfatlevels",
                    "sugarslevels": "$sugarslevels",
                },
                "count": {"$sum": 1},
            }},
        ]

        listRes = []
        for doc in mongo.db.products.aggregate(pipeline):
            res = {}
            res['dateyear'] = doc['_id']['year']
            res['datemonth'] = doc['_id']['month']
            res['count'] = doc['count']
            res['saltlevels'] = doc['_id']['saltlevels']
            res['saturatedfatlevels'] = doc['_id']['saturatedfatlevels']
            res['sugarslevels'] = doc['_id']['sugarslevels']
            res['fatlevels'] = doc['_id']['fatlevels']
            listRes.append(res)
        return listRes


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
            # Aggregation replacement for the old map_reduce over the
            # 'brands' field (removed in PyMongo 4.0).
            pipeline = [
                {"$match": {"brands": {"$type": "string"}}},
                {"$group": {"_id": {"$trim": {"input": "$brands"}}}},
                {"$match": {"_id": {"$regex": query, "$options": "i"}}},
                {"$sort": {"_id": 1}},
            ]

            res = []
            for doc in mongo.db.products.aggregate(pipeline):
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


# ----- /products/categories -----
class ProductsCategories(restful.Resource):

    # ----- GET Request -----
    def get(self):
        # ----- Get count # in the request, 0 by default -----
        count = request.args.get('count',default=0, type=int)
        query = request.args.get('query')

        if request.args.get('query'):
            # Aggregation replacement for the old map_reduce over the
            # 'categories' field (removed in PyMongo 4.0).
            pipeline = [
                {"$match": {"categories": {"$type": "string"}}},
                {"$group": {"_id": {"$trim": {"input": "$categories"}}}},
                {"$match": {"_id": {"$regex": query, "$options": "i"}}},
                {"$sort": {"_id": 1}},
            ]

            res = []
            for doc in mongo.db.products.aggregate(pipeline):
                res.append(doc['_id'])
            if request.args.get('count') and count == 1:
                return len(res)
            else:
                return res
        else:
            if request.args.get('count') and count == 1:
                return  len(mongo.db.products.distinct('categories'))
            else:
                return  mongo.db.products.distinct('categories')


# ----- /products/countries -----
class ProductsCountries(restful.Resource):

    # ----- GET Request -----
    def get(self):
        # ----- Get count # in the request, 0 by default -----
        count = request.args.get('count',default=0, type=int)
        query = request.args.get('query')

        if request.args.get('query'):
            # Aggregation replacement for the old map_reduce over the
            # 'countries' field (removed in PyMongo 4.0).
            pipeline = [
                {"$match": {"countries": {"$type": "string"}}},
                {"$group": {"_id": {"$trim": {"input": "$countries"}}}},
                {"$match": {"_id": {"$regex": query, "$options": "i"}}},
                {"$sort": {"_id": 1}},
            ]

            res = []
            for doc in mongo.db.products.aggregate(pipeline):
                res.append(doc['_id'])
            if request.args.get('count') and count == 1:
                return len(res)
            else:
                return res
        else:
            if request.args.get('count') and count == 1:
                return  len(mongo.db.products.distinct('countries'))
            else:
                return  mongo.db.products.distinct('countries')


# ----- /products/additives -----
class ProductsAdditives(restful.Resource):

    # ----- GET Request -----
    def get(self):
        # ----- Get count # in the request, 0 by default -----
        count = request.args.get('count',default=0, type=int)
        query = request.args.get('query')

        if request.args.get('query'):
            # Aggregation replacement for the old map_reduce over the
            # 'additives_tags' array (removed in PyMongo 4.0).
            # Note: the old JS guarded on `this.colours` (likely a
            # copy-paste bug) while iterating `additives_tags`; the
            # guard is intentionally not carried over.
            pipeline = [
                {"$match": {"additives_tags": {"$type": "array"}}},
                {"$unwind": "$additives_tags"},
                {"$match": {"additives_tags": {"$type": "string"}}},
                {"$group": {"_id": {"$trim": {"input": "$additives_tags"}}}},
                {"$match": {"_id": {"$regex": query, "$options": "i"}}},
                {"$sort": {"_id": 1}},
            ]

            res = []
            for doc in mongo.db.products.aggregate(pipeline):
                res.append(doc['_id'])
            if request.args.get('count') and count == 1:
                return len(res)
            else:
                return res
        else:
            if request.args.get('count') and count == 1:
                return  len(mongo.db.products.distinct('additives_tags'))
            else:
                return  mongo.db.products.distinct('additives_tags')


# ----- /products/allergens -----
class ProductsAllergens(restful.Resource):

    # ----- GET Request -----
    def get(self):
        # ----- Get count # in the request, 0 by default -----
        count = request.args.get('count',default=0, type=int)
        query = request.args.get('query')

        if request.args.get('query'):
            # Aggregation replacement for the old map_reduce over the
            # 'allergens_tags' array (removed in PyMongo 4.0).
            # Note: the old JS guarded on `this.colours` (likely a
            # copy-paste bug) while iterating `allergens_tags`; the
            # guard is intentionally not carried over.
            pipeline = [
                {"$match": {"allergens_tags": {"$type": "array"}}},
                {"$unwind": "$allergens_tags"},
                {"$match": {"allergens_tags": {"$type": "string"}}},
                {"$group": {"_id": {"$trim": {"input": "$allergens_tags"}}}},
                {"$match": {"_id": {"$regex": query, "$options": "i"}}},
                {"$sort": {"_id": 1}},
            ]

            res = []
            for doc in mongo.db.products.aggregate(pipeline):
                res.append(doc['_id'])
            if request.args.get('count') and count == 1:
                return len(res)
            else:
                return res
        else:
            if request.args.get('count') and count == 1:
                return  len(mongo.db.products.distinct('allergens_tags'))
            else:
                return  mongo.db.products.distinct('allergens_tags')



api.add_resource(ProductsList, '/products')
api.add_resource(ProductsStats, '/products/stats/info')
api.add_resource(ProductId, '/product/<string:barcode>')
api.add_resource(ProductsBrands, '/products/brands')
api.add_resource(ProductsCategories, '/products/categories')
api.add_resource(ProductsCountries, '/products/countries')
api.add_resource(ProductsAdditives, '/products/additives')
api.add_resource(ProductsAllergens, '/products/allergens')