from flask import Flask
from flask_restful import Api  #Resources are usally mapped into db tables
# JWT is stands for json web token for user-authentication
from flask_jwt import JWT
from security import authenticate, identity
from resources.item import Item, ItemList
from resources.user import UserRegister
from resources.store import Store, StoreList
from db import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///data.db'
# To do not track the Object which is created but not stored in db
# It turn off flask-SQLAlchemy but does not off underlying SQLAlchemy modification tracker
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
# app.config['TESTING'] = True
app.secret_key = 'Cas@1234'
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWT(app, authenticate, identity) #creates new endpoint "/auth"


api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    db.init_app(app)
    app.run(debug=True)
