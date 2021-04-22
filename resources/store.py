from flask_restful import Resource, reqparse
from models.store_model import StoreModel
from flask_jwt import jwt_required


class Store(Resource):

    parser = reqparse.RequestParser()

    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {'message': 'Store not found'}, 404

    def post(self,name):
        store = StoreModel.find_by_name(name)
        if store:
            return {'message': "Store already exist..."}
        store = StoreModel(name)
        print(store.name)
        try:
            store.save_to_db()
        except Exception as e:
            return {'message': 'An error occurred while creating the store'}, 500
        return store.json(), 201

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete()
            return {'message': 'Store deleted.'}
        else:
            return {'message': 'Store not exist'}


class StoreList(Resource):
    def get(self):
        return {'Stores': [store.json() for store in StoreModel.query.all()]}
