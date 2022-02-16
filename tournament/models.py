from tournament import db

class Item(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    surname = db.Column(db.Integer(), nullable=False)
    points = db.Column(db.String(length=12), nullable=False, unique=True)

    def __repr__(self):
        return f'Item {self.name}'
