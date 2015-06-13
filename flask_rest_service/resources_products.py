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
                return mongo.db.products.find(data, fieldsNeeded).count()
            elif not request.args.get('count') and not request.args.get('q'):
                return mongo.db.products.find(data, fieldsNeeded).sort('created_t', pymongo.DESCENDING).skip(skip).limit(limit)
            elif request.args.get('count') and count == 1 and request.args.get('q'):
                return mongo.db.products.find({ "$text" : { "$search": query } }, fieldsNeeded).count()
            else:
                return mongo.db.products.find({ "$text" : { "$search": query } }, fieldsNeeded).sort('created_t', pymongo.DESCENDING).skip(skip).limit(limit)
        else:
            if request.args.get('count') and count == 1 and not request.args.get('q'):
                return mongo.db.products.find(data).count()
            elif not request.args.get('count') and not request.args.get('q'):
                return mongo.db.products.find(data).sort('created_t', pymongo.DESCENDING).skip(skip).limit(limit)
            elif request.args.get('count') and count == 1 and request.args.get('q'):
                return mongo.db.products.find({ "$text" : { "$search": query } }).count()
            else:
                return mongo.db.products.find({ "$text" : { "$search": query } }).sort('created_t', pymongo.DESCENDING).skip(skip).limit(limit)


# ----- /products/all-----
class ProductsStats(restful.Resource):

    # ----- GET Request -----
    def get(self):
        date = request.args.get('dateby',default=0, type=int)

        # By year
        if date == 0 : 
            map = Code("function () {"
                            "   var date = new Date(this.created_t*1000);"
                            "   var parsedDateYear = date.getFullYear();"
                            "   if(!parsedDateYear) return;"
                            "   emit({year : parsedDateYear}, {count:1});"
                            "};")
        #By year & month
        elif date == 1 :
            map = Code("function () {"
                            "   var date = new Date(this.created_t*1000);"
                            "   var parsedDateMonth = date.getMonth();"
                            "   var parsedDateYear = date.getFullYear();"
                            "   if(!parsedDateYear || !parsedDateMonth) return;"
                            "   emit({year : parsedDateYear, month : parsedDateMonth}, {count:1});"
                            "};")
        #By year & month & day
        elif date == 2 :
            map = Code("function () {"
                            "   var date = new Date(this.created_t*1000);"
                            "   var parsedDateMonth = date.getMonth();"
                            "   var parsedDateYear = date.getFullYear();"
                            "   var parsedDateDay = date.getDay();"
                            "   if(!parsedDateYear || !parsedDateMonth || !parsedDateDay) return;"
                            "   emit({year : parsedDateYear, month : parsedDateMonth, day : parsedDateDay}, {count:1});"
                            "};")


        reduce = Code("function (key, values) {"
                    "   var count = 0;"
                    "   var ret = {count : 0};"
                    "       for (index in values) {"
                    "           ret.count += values[index].count;"
                    "       }"
                    "       return ret;"    
                    "   };")

        result = mongo.db.products.map_reduce(map, reduce, "stats_products")
        return result.find()


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


# ----- /products/categories -----
class ProductsCategories(restful.Resource):

    # ----- GET Request -----
    def get(self):
        # ----- Get count # in the request, 0 by default -----
        count = request.args.get('count',default=0, type=int)
        query = request.args.get('query')

        if request.args.get('query'):
            map = Code("function () {"
                        "   if (!this.categories) return;"
                        "   emit(this.categories.trim(), 1);"
                        "};")

            reduce = Code("function (key, values) {"
                        "   var count = 0;"
                        "       for (index in values) {"
                        "           count += values[index];"
                        "       }"
                        "       return count;"    
                        "   };")

            result = mongo.db.products.map_reduce(map, reduce, "categories_products")

            res = []
            for doc in result.find({"_id": {'$regex' : query, '$options' : '-i'}}):
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
            map = Code("function () {"
                        "   if (!this.countries) return;"
                        "   emit(this.countries.trim(), 1);"
                        "};")

            reduce = Code("function (key, values) {"
                        "   var count = 0;"
                        "       for (index in values) {"
                        "           count += values[index];"
                        "       }"
                        "       return count;"    
                        "   };")

            result = mongo.db.products.map_reduce(map, reduce, "countries_products")

            res = []
            for doc in result.find({"_id": {'$regex' : query, '$options' : '-i'}}):
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
            map = Code("function () {"
                        "   if (!this.colours) return;"
                        "   this.additives_tags.forEach(function (c){"
                        "       emit(c.trim(), 1)"
                        "   });"
                        "};")

            reduce = Code("function (key, values) {"
                        "   var count = 0;"
                        "       for (index in values) {"
                        "           count += values[index];"
                        "       }"
                        "       return count;"    
                        "   };")

            result = mongo.db.products.map_reduce(map, reduce, "additives_products")

            res = []
            for doc in result.find({"_id": {'$regex' : query, '$options' : '-i'}}):
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
            map = Code("function () {"
                        "   if (!this.colours) return;"
                        "   this.allergens_tags.forEach(function (c){"
                        "       emit(c.trim(), 1)"
                        "   });"
                        "};")

            reduce = Code("function (key, values) {"
                        "   var count = 0;"
                        "       for (index in values) {"
                        "           count += values[index];"
                        "       }"
                        "       return count;"    
                        "   };")

            result = mongo.db.products.map_reduce(map, reduce, "allergens_products")

            res = []
            for doc in result.find({"_id": {'$regex' : query, '$options' : '-i'}}):
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
api.add_resource(ProductsStats, '/products/stats')
api.add_resource(ProductId, '/product/<string:barcode>')
api.add_resource(ProductsBrands, '/products/brands')
api.add_resource(ProductsCategories, '/products/categories')
api.add_resource(ProductsCountries, '/products/countries')
api.add_resource(ProductsAdditives, '/products/additives')
api.add_resource(ProductsAllergens, '/products/allergens')