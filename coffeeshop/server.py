#!.venv/bin/python

from flask import Flask, jsonify, abort, make_response
from flask.ext.restful import Api, Resource, reqparse, fields, marshal

app = Flask(__name__, static_url_path="")
api = Api(app)

coffee_list = [
    {
        'id': 1,
        'title': u'Latte',
        'description': u'Rich and Creamy Coffee',
        'price': 3.5
    },
    {
        'id': 2,
        'title': u'Mocha',
        'description': u'Coffee with a dash of Chocolate',
        'price': 4.75
    },
    {
        'id': 3,
        'title': u'Espresso',
        'description': u'Dark & invigorating',
        'price': 3.00
    }
]

coffee_fields = {
    'title': fields.String,
    'description': fields.String,
    'price': fields.Float,
    'uri': fields.Url('coffee')
}


class CoffeeListAPI(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type=str, required=True,
                                   help='No coffee title provided',
                                   location='json')
        self.reqparse.add_argument('description', type=str, default="",
                                   location='json')
        self.reqparse.add_argument('price', type=float, required=True,
                                   help='No coffee price provided',
                                   location='json')
        super(CoffeeListAPI, self).__init__()

    # curl -i http://localhost:5000/todo/api/v1.0/coffee
    def get(self):
        return {'coffee': [marshal(coffee, coffee_fields) for coffee in coffee_list]}

    # curl -i -H "Content-Type: application/json" -X POST -d '{"title":"Spiced Latte", "price": 4.95}' http://localhost:5000/todo/api/v1.0/coffee
    def post(self):
        args = self.reqparse.parse_args()
        coffee = {
            'id': coffee_list[-1]['id'] + 1,
            'title': args['title'],
            'description': args['description'],
            'price': args['price']
        }
        coffee_list.append(coffee)
        return {'coffee': marshal(coffee, coffee_fields)}, 201


class CoffeeAPI(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type=str, location='json')
        self.reqparse.add_argument('description', type=str, location='json')
        self.reqparse.add_argument('price', type=float, location='json')
        super(CoffeeAPI, self).__init__()

    # curl -i http://localhost:5000/todo/api/v1.0/coffee/1
    def get(self, id):
        coffee = [coffee for coffee in coffee_list if coffee['id'] == id]
        if len(coffee) == 0:
            abort(404)
        return {'coffee': marshal(coffee[0], coffee_fields)}

    # curl -i -H "Content-Type: application/json" -X PUT -d '{"price":4.85}' http://localhost:5000/todo/api/v1.0/coffee/2
    def put(self, id):
        coffee = [coffee for coffee in coffee_list if coffee['id'] == id]
        if len(coffee) == 0:
            abort(404)
        coffee = coffee[0]
        args = self.reqparse.parse_args()
        for k, v in args.items():
            if v is not None:
                coffee[k] = v
        return {'coffee': marshal(coffee, coffee_fields)}

    # curl -i -X DELETE http://localhost:5000/todo/api/v1.0/coffee/1
    def delete(self, id):
        coffee = [coffee for coffee in coffee_list if coffee['id'] == id]
        if len(coffee) == 0:
            abort(404)
        coffee_list.remove(coffee[0])
        return {'result': True}


api.add_resource(CoffeeListAPI, '/todo/api/v1.0/coffee', endpoint='coffee_list')
api.add_resource(CoffeeAPI, '/todo/api/v1.0/coffee/<int:id>', endpoint='coffee')

if __name__ == '__main__':
    app.run(debug=True)