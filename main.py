from app import app
from app import db
from app import User
from datetime import datetime
import calendar
import locale


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

locale.setlocale(locale.LC_ALL, 'uk_UA.UTF-8')
def month_number_to_name(month_number):
    month_number = int(month_number)
    return calendar.month_name[month_number]

month = f'{datetime.today().month-1:02}' if datetime.today().month-1 < 10 else str(datetime.today().month-1)

print(month_number_to_name(month))