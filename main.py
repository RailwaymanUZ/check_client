from app import app
from app import db
from app import User
from datetime import datetime

''' добавление нового пользователя
with app.app_context():
    user = User(login='luda', password='ilovebinotel')

    db.session.add(user)
    db.session.commit()
'''
'''
with app.app_context():
    db.create_all()
'''

month = f'{datetime.today().month:02}' if datetime.today().month < 10 else str(datetime.today().month)


print(month)