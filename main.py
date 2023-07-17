from app import app
from app import db
from app import User

with app.app_context():
    user = User(login='luda', password='ilovebinotel')

    db.session.add(user)
    db.session.commit()
