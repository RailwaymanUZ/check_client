from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from db import value_to_db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///client.db'
db = SQLAlchemy(app)


class Client(db.Model):
    id = db.Column(db.Integer, primary_key=False)
    name_company = db.Column(db.String(100), primary_key=True)
    number_docs = db.Column(db.String(100), primary_key=True)
    company_details = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return '<Client &r>' % self.id


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_client', methods=['POST', 'GET'])
def add_client():
    if request.method == 'POST':
        name_company = request.form['name_company']
        if value_to_db(name_company) != True:
            return render_template('error_page.html')

        number_doc = request.form['number_docs']
        if value_to_db(number_doc) != True:
            return render_template('error_page.html')

        company_details = request.form['company_details']
        if value_to_db(company_details) != True:
            return render_template('error_page.html')
        # id клиента надо заменить на пользователя
        client = Client(id=1,name_company=name_company, number_docs=number_doc, company_details=company_details)
        try:
            db.session.add(client)
            db.session.commit()
            return redirect('/') # перенаправляем на станичку
        except:
            return 'При додаванні клієнта виникла помилка'

    else:
        return render_template('add_client.html')

@app.route('/all_client')
def all_client():
    client = Client.query.all()
    return render_template('all_client.html', client=client)

@app.route('/delete_client', methods=['POST'])
def delete_client():
    name_company = request.form['name_company']
    number_docs = request.form['number_docs']
    company_details = request.form['company_details']

    print(name_company)
    print(number_docs)
    print(company_details)

    return redirect('/all_client')


if __name__ == '__main__':
    app.run(debug=True)
