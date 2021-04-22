from flask_restful import Resource, reqparse #Resources are usally mapped into db tables
from flask_jwt import jwt_required
from models.item_model import ItemModel


# The API works with resources and every resource has to be a class
class Item(Resource):
    parser = reqparse.RequestParser()  # Creating the object of "RequestParser" which we used to parse the request
    parser.add_argument('price', type=float, required=True,
                        help='This field can not be left blank')
    parser.add_argument('store_id', type=int, required=True,
                        help='Every item needs a store id.')
    # def get(self, name):
    #     for item in items:
    #         if item['name'] == name:
    #             return item
    #     return {'item': None}, 404

    @jwt_required() # We have to authenticate before going to api
    def get(self, name):
        # item = next(filter(lambda x: x['name'] == name, items), None)
        # return {'item': item}, 200 if item is not None else 404

        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    def post(self,name):
        item = ItemModel.find_by_name(name)
        if item:
            return {'message':'An item with name {}, is already exist'.format(name)}, 400

        data = Item.parser.parse_args()
        item = ItemModel(name, data['price'], data['store_id'])
        try:
            item.save_to_db()
        except Exception as e:
            return {'message': 'An error occurred while inserting an item'}, 500
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        # query = "INSERT INTO items VALUES (?, ?)"
        #
        # cursor.execute(query, (name, data['price']))
        # connection.commit()
        # connection.close()
        return item.json(), 201

    def delete(self, name):
        # global items
        # items = list(filter(lambda x:x['name'] != name, items))
        # connection = sqlite3.connect('../data.db')
        # cursor = connection.cursor()
        # query = "DELETE FROM items WHERE name=?"
        #
        # cursor.execute(query, (name,))
        # connection.commit()
        # connection.close()
        # return {'message': 'Item deleted'}
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {'message': 'Item deleted'}

    # Way one
    # def put(self,name):
    #
    #     item = Item.find_by_name(name)
    #     data = Item.parser.parse_args()
    #     # item = next(filter(lambda x:x['name'] == name, items), None)
    #     connection = sqlite3.connect('data.db')
    #     cursor = connection.cursor()
    #     if item:
    #         query = "UPDATE items SET price = ? WHERE name = ?"
    #         cursor.execute(query, (data['price'], name))
    #
    #     item = {'name': name, 'price': data['price']}
    #     query = "INSERT INTO items VALUES (?, ?)"
    #     cursor.execute(query, (item['name'], item['price']))
    #
    #     connection.commit()
    #     connection.close()
    #
    #     return {'message': 'Success'}
        # End of put method way one

    # Way two (here we have to create two class methods "insert"&"update")
    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        # updated_item = ItemModel(name, data['price'])

        if item is None:
            item = ItemModel(name, data['price'], data['store_id'])
            # updated_item.insert()

        else:
            item.price = data['price']
            # updated_item.update()

        item.save_to_db()
        return item.json()


class ItemList(Resource):
    def get(self):
        print("Hi")
        return {'items': [item.json() for item in ItemModel.query.all()]}
        # return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}
        print("Bye")

