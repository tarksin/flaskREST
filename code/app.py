from flask import Flask, request
from flask_restful import Resource, Api
from flask_jwt import  JWT, jwt_required

from security import authenticate, identity

app = Flask(__name__)
app.secret_key='65aaedd7-d0f8-4e5f-9df1-38faabad721d'
api = Api(app)


jwt = JWT(app, authenticate, identity)  # /auth  end point

organisms = []
#{"name":"Birds",
#        "organisms":[
#            {"name":"Anas platyrhynchos","common_name":"Mallard"},
#            {"name":"Calypte anna","common_name":"Anna's hummingbird "},


class Organism(Resource):
    @jwt_required()
    def get(self, name):
        organism = next(filter(lambda x: x['name'] == name, organisms), None)
        return {'organism':organism}, 200 if organism  else 404

        # for organism in organisms:
        #     if organism["name"] == name:
        #         return organism


    def post(self, name):
        if next(filter(lambda x: x['name'] == name, organisms), None):
            return{'message':'{} is already in the database'.format(name)}, 400
        request_data = request.get_json()
        organism = {"name":name, "common_name":  request_data["common_name"]}
        organisms.append(organism)
        return organism, 201

    def delete(self, name):
        global organisms
        organisms = list(filter( lambda x: x['name'] != name, organisms))
        return {'message':'Item deleted'}

class ItemList(Resource):
    def get(self):
        return {'organisms':organisms}


#http://127.0.0.1/organism/"Coturnix japonica"
api.add_resource(Organism, '/organism/<string:name>')
api.add_resource(ItemList, '/organisms')

app.run(port=3005, debug=True)
