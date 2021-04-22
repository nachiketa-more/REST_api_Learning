from db import db


class StoreModel(db.Model):
    __tablename__ = 'store'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    # Whenever Store Model is created we create a object of each item of ItemModel belongs to the specific store id.
    # items = db.relationship('ItemModel')
    # lazy='dynamic' disable above scenario
    items = db.relationship('ItemModel', lazy='dynamic')

    def __init__(self, name):
        self.name = name

    # Here items have lazy parameter so here items is not the list of item objects
    # Whenever we call the json() only that time the item object is created
    # Here self.items is act like a query builder and to fetch the all item object we have to use all()
    def json(self):
        return {'name': self.name, 'items': [item.json for item in self.items.all()]}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
