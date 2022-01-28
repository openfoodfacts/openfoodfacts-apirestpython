# Open Food Facts API Rest Python

OFF API provides programmatic access to Open Food Facts functionality and content.<br/>

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/openfoodfacts/OpenFoodFacts-APIRestPython)

To try the API : https://openfoodfacts-api.herokuapp.com/ <br/>
Or if you want to try in localhost, see below.

The API is [REST API](https://en.wikipedia.org/wiki/Representational_State_Transfer "RESTful").
Currently, return format for all endpoints is [JSON](https://json.org/ "JSON").

## Status


[![Project Status](http://opensource.box.com/badges/active.svg)](http://opensource.box.com/badges)
[![Build Status](https://travis-ci.org/openfoodfacts/OpenFoodFacts-APIRestPython.svg?branch=master)](https://travis-ci.org/openfoodfacts/OpenFoodFacts-APIRestPython)
[![Average time to resolve an issue](https://isitmaintained.com/badge/resolution/openfoodfacts/OpenFoodFacts-APIRestPython.svg)](https://isitmaintained.com/project/openfoodfacts/OpenFoodFacts-APIRestPython "Average time to resolve an issue")
[![Percentage of issues still open](https://isitmaintained.com/badge/open/openfoodfacts/OpenFoodFacts-APIRestPython.svg)](https://isitmaintained.com/project/openfoodfacts/OpenFoodFacts-APIRestPython "Percentage of issues still open")

## What is this repository for?

This piece of software’s main goals are:
* To make it easy to retrieve data using HTTP requests
* To provide filters in the API
* To provide custom filters


## Setup for localhost

* Install python 3
* Install mongodb
* Install pip
* Install requirements: `$ pip install -r requirements.txt`
* Download the database from : https://world.openfoodfacts.org/data/openfoodfacts-mongodbdump.tar.gz
* Import to local mongodb: `$ mongorestore -d off -c products /foldertobsonfile/products.bson`
* Launch api: `$ python3 runApiRESTServer.py`
* That's all!

## Documentation
### How to use it?

Simple filter: `/products?origins=United Kingdom` <br/>
Complex filter: `/products?nutrition_grade_fr=a&origins=United Kingdom` <br/>
For arrays, a “.” will be used as a separator like so: `/products?nutrient_levels.salt=low`
Searchs can be inexact like :`/products?ingredients_text=beef`<br/>
It will retrieve tags like “beef braising steak”, “beef steak”...

/!\ By default the objects will be sorted by `created_t` in order to have the most important objects first

URL to query                   | Description
------------------------------ | ---------------------------
<code>GET</code> `/product/<barcode>`           | Get a product by barcode eg. `/product/737628064502`
<code>GET</code> `/products/brands`             | Return a list of `Brands`. If you want to query brands, to do for example an autocomplete field in ajax, query the API like: `/products/brands?query=Auch` or `/products/brands?query=Sains`.
<code>GET</code> `/products/categories`         | Return a list of `Categories`. If you want to query categories, to do for example an autocomplete field in ajax, query the API like: `/products/categories?query=Ric` or `/products/categories?query=plant`.
<code>GET</code> `/products/countries`          | Return a list of `Countries`. If you want to query countries, to do for example an autocomplete field in ajax, query the API like: `/products/countries?query=Fra` or `/products/countries?query=Aus`.
<code>GET</code> `/products/additives`          | Return a list of `Additives`. If you want to query additives, to do for example an autocomplete field in ajax, query the API like: `/products/additives?query=Citric` or `/products/additives?query=acid`.
<code>GET</code> `/products/allergens`          | Return a list of `Allergens`. If you want to query allergens, to do for example an autocomplete field in ajax, query the API like: `/products/allergens?query=milk` or `/products/allergens?query=oil`.

### Options

Field         | Value by default | Value type
------------- | ---------------- | ---------
limit=        | 50               | limit the number of products returned
skip=         | 0                | skips the specified number of products returned
count=        | 0                | if 1 then returns the number of rows
short=        | 0                | Filters rows retrieved, make it faster for lists for example, if 1 columns projection on `code`, `lang` and `product_name`
q=            | none             | search text on indexed fields

### Indexed fields

Some fields are described here: https://world.openfoodfacts.org/data/data-fields.txt

### Example
**Request**

    GET /product/737628064502

**Return**
``` json
{
   "status_verbose":"product found",
   "status":1,
   "product":{
      "last_edit_dates_tags":[
         "2012-12-11",
         "2012-12",
         "2012"
      ],
      "labels_hierarchy":[
         "en:gluten-free"
      ],
      "_id":"737628064502",
      "categories_hierarchy":[
         "en:Rice Noodles"
      ],
      "pnns_groups_1":"unknown",
      "states_tags":[
         "en:to-be-checked",
         "en:complete",
         "en:nutrition-facts-completed",
         "en:ingredients-completed",
         "en:expiration-date-to-be-completed",
         "en:characteristics-completed",
         "en:photos-validated",
         "en:photos-uploaded"
      ],
      "checkers_tags":[
      ],
      "labels_tags":[
         "en:gluten-free"
      ],
      "image_small_url":"https://world.openfoodfacts.org/images/products/737/628/064/502/front.6.200.jpg",
      "code":"737628064502",
      "additives_tags_n":null,
      "traces_tags":[
         "peanuts"
      ],
      "lang":"en",
      "photographers":[
         "andre"
      ],
      "generic_name":"Rice Noodles",
      "ingredients_that_may_be_from_palm_oil_tags":[
      ],
      "old_additives_tags":[
         "en:e330"
      ],
      "_keywords":[
         "thailand",
         "stir-fry",
         "kitchen",
         "thai",
         "free",
         "gluten",
         "rice",
         "noodle"
      ],
      "rev":15,
      "editors":[
         "",
         "thierrym",
         "manu1400",
         "andre"
      ],
      "interface_version_created":"20120622",
      "emb_codes":"",
      "max_imgid":"5",
      "additives_tags":[
         "en:e330"
      ],
      "emb_codes_orig":"",
      "informers_tags":[
         "andre",
         "manu1400",
         "thierrym"
      ],
      "nutrient_levels_tags":[
         "脂肪-in-moderate-quantity",
         "饱和脂肪-in-low-quantity",
         "糖-in-high-quantity",
         "食盐-in-high-quantity"
      ],
      "photographers_tags":[
         "andre"
      ],
      "additives_n":1,
      "pnns_groups_2_tags":[
         "unknown"
      ],
      "unknown_nutrients_tags":[
      ],
      "packaging_tags":[
         "cellophane",
         "carton"
      ],
      "nutriments":{
         "sodium":"0.629",
         "sugars":10,
         "carbohydrates_unit":"g",
         "fat_unit":"g",
         "proteins_unit":"g",
         "nutrition-score-fr_100g":15,
         "fat":7,
         "proteins_serving":7,
         "sodium_serving":0.629,
         "salt":1.59766,
         "proteins":7,
         "nutrition-score-fr":15,
         "sugars_unit":"g",
         "fat_serving":7,
         "sodium_unit":"mg",
         "sugars_100g":"12.8",
         "saturated-fat_unit":"g",
         "sodium_100g":0.806,
         "saturated-fat_serving":1,
         "fiber_unit":"g",
         "energy":1297,
         "energy_unit":"kcal",
         "sugars_serving":10,
         "carbohydrates_100g":70.5,
         "nutrition-score-uk":15,
         "proteins_100g":8.97,
         "fiber_serving":0,
         "carbohydrates_serving":55,
         "energy_serving":1297,
         "fat_100g":"8.97",
         "saturated-fat_100g":"1.28",
         "nutrition-score-uk_100g":15,
         "fiber":0,
         "salt_serving":1.59766,
         "salt_100g":"2.05",
         "carbohydrates":55,
         "fiber_100g":0,
         "energy_100g":1660,
         "saturated-fat":1
      },
      "countries_tags":[
         "en:france"
      ],
      "ingredients_from_palm_oil_tags":[
      ],
      "emb_codes_tags":[
      ],
      "brands_tags":[
         "thai-kitchen"
      ],
      "purchase_places":"",
      "pnns_groups_2":"unknown",
      "countries_hierarchy":[
         "en:france"
      ],
      "traces":"Peanuts",
      "categories":"Rice Noodles",
      "ingredients_text":"RICE NOODLES (RICE, WATER), SEASONING PACKET (PEANUT, SUGAR, SALT, CORN STARCH, SPICES [CHILI, CINNAMON, PEPPER, CUMIN, CLOVE], HYDRDLYZED SOY PROTEIN, GREEN ONIONS, CITRIC ACID, PEANUT OIL, SESAME OIL, NATURAL FLAVOR).  ",
      "created_t":1345799269,
      "product_name":"Stir-Fry Rice Noodles",
      "ingredients_from_or_that_may_be_from_palm_oil_n":0,
      "creator":"andre",
      "no_nutrition_data":null,
      "serving_size":"78 g",
      "completed_t":1355184837,
      "last_modified_by":"thierrym",
      "new_additives_n":1,
      "origins":"Thailand",
      "stores":"",
      "nutrition_grade_fr":"d",
      "nutrient_levels":{
         "salt":"high",
         "fat":"moderate",
         "sugars":"high",
         "saturated-fat":"low"
      },
      "stores_tags":[
      ],
      "id":"737628064502",
      "countries":"France",
      "purchase_places_tags":[
      ],
      "interface_version_modified":"20120622",
      "fruits-vegetables-nuts_100g_estimate":0,
      "sortkey":1355184837,
      "last_modified_t":1355184837,
      "nutrition_score_debug":" -- energy 4 + sat-fat 1 + fr-sat-fat-for-fats 0 + sugars 2 + sodium 8 - fruits 0% 0 - fiber 0 - proteins 5 -- fsa 15 -- fr 15",
      "countries.20131227":null,
      "correctors_tags":[
         "andre",
         "thierrym"
      ],
      "correctors":[
         "andre",
         "thierrym"
      ],
      "new_additives_debug":"lc: en -  [ rice-noodles -> en:rice-noodles  ]  [ rice -> en:rice  ]  [ water -> en:water  ]  [ seasoning-packet -> en:seasoning-packet  ]  [ peanut -> en:peanut  ]  [ sugar -> en:sugar  ]  [ salt -> en:salt  ]  [ corn-starch -> en:corn-starch  ]  [ spices-chili -> en:spices-chili  ]  [ cinnamon -> en:cinnamon  ]  [ pepper -> en:pepper  ]  [ cumin -> en:cumin  ]  [ clove -> en:clove  ]  [ hydrdlyzed-soy-protein -> en:hydrdlyzed-soy-protein  ]  [ green-onions -> en:green-onions  ]  [ citric-acid -> en:e330  -> exists  ]  [ peanut-oil -> en:peanut-oil  ]  [ sesame-oil -> en:sesame-oil  ]  [ natural-flavor -> en:natural-flavor  ] ",
      "brands":"Thai Kitchen",
      "ingredients_tags":[
         "rice-noodles",
         "seasoning-packet",
         "",
         "rice",
         "water",
         "peanut",
         "sugar",
         "salt",
         "corn-starch",
         "spices",
         "chili",
         "cinnamon",
         "pepper",
         "cumin",
         "clove",
         "hydrdlyzed-soy-protein",
         "green-onions",
         "citric-acid",
         "peanut-oil",
         "sesame-oil",
         "natural-flavor"
      ],
      "new_additives_tags":[
         "en:e330"
      ],
      "states":"en:to-be-checked, en:complete, en:nutrition-facts-completed, en:ingredients-completed, en:expiration-date-to-be-completed, en:characteristics-completed, en:photos-validated, en:photos-uploaded",
      "informers":[
         "andre",
         "manu1400",
         "thierrym"
      ],
      "entry_dates_tags":[
         "2012-08-24",
         "2012-08",
         "2012"
      ],
      "nutrition_grades_tags":[
         "d"
      ],
      "packaging":"Cellophane,Carton",
      "serving_quantity":78,
      "origins_tags":[
         "thailand"
      ],
      "nutrition_data_per":"serving",
      "labels":"gluten free",
      "cities_tags":[
      ],
      "emb_codes_20141016":"",
      "categories_tags":[
         "en:rice-noodles"
      ],
      "quantity":"155 g",
      "expiration_date":"",
      "states_hierarchy":[
         "en:to-be-checked",
         "en:complete",
         "en:nutrition-facts-completed",
         "en:ingredients-completed",
         "en:expiration-date-to-be-completed",
         "en:characteristics-completed",
         "en:photos-validated",
         "en:photos-uploaded"
      ],
      "ingredients_that_may_be_from_palm_oil_n":0,
      "ingredients_from_palm_oil_n":0,
      "image_url":"https://world.openfoodfacts.org/images/products/737/628/064/502/front.6.400.jpg",
      "ingredients":[
         {
            "text":"RICE NOODLES",
            "id":"rice-noodles",
            "rank":1
         },
         {
            "text":"SEASONING PACKET",
            "id":"seasoning-packet",
            "rank":2
         },
         {
            "text":".",
            "id":"",
            "rank":3
         },
         {
            "text":"RICE",
            "id":"rice"
         },
         {
            "text":"WATER",
            "id":"water"
         },
         {
            "text":"PEANUT",
            "id":"peanut"
         },
         {
            "text":"SUGAR",
            "id":"sugar"
         },
         {
            "text":"SALT",
            "id":"salt"
         },
         {
            "text":"CORN STARCH",
            "id":"corn-starch"
         },
         {
            "text":"SPICES",
            "id":"spices"
         },
         {
            "text":"CHILI",
            "id":"chili"
         },
         {
            "text":"CINNAMON",
            "id":"cinnamon"
         },
         {
            "text":"PEPPER",
            "id":"pepper"
         },
         {
            "text":"CUMIN",
            "id":"cumin"
         },
         {
            "text":"CLOVE",
            "id":"clove"
         },
         {
            "text":"HYDRDLYZED SOY PROTEIN",
            "id":"hydrdlyzed-soy-protein"
         },
         {
            "text":"GREEN ONIONS",
            "id":"green-onions"
         },
         {
            "text":"CITRIC ACID",
            "id":"citric-acid"
         },
         {
            "text":"PEANUT OIL",
            "id":"peanut-oil"
         },
         {
            "text":"SESAME OIL",
            "id":"sesame-oil"
         },
         {
            "text":"NATURAL FLAVOR",
            "id":"natural-flavor"
         }
      ],
      "lc":"en",
      "pnns_groups_1_tags":[
         "unknown"
      ],
      "checkers":[
      ],
      "complete":1
   },
   "code":"737628064502"
}
```

## Creators

**Scot Scriven**
- <https://github.com/itchix>

## Copyright and license

    Copyright 2015 Scriven Scot

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        https://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
