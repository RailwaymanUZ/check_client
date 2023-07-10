from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from db import value_to_db
from docx import Document


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
    del_client = Client.query.filter_by(name_company=name_company, number_docs=number_docs,
                                        company_details=company_details).first()
    if del_client:
        db.session.delete(del_client)
        db.session.commit()

    return redirect('/all_client')


@app.route('/edit_client', methods=['POST'])
def edit_client():
    hiden_information = request.form['hiden_information']
    if hiden_information == 'first_vision':
        name_company = request.form['name_company']
        number_docs = request.form['number_docs']
        company_details = request.form['company_details']
        old_client = Client(name_company=name_company, number_docs=number_docs, company_details=company_details)

        return render_template('edit_client.html', old_client=old_client)

    if hiden_information == 'chenge':
        old_name_company = request.form['old_name_company']
        old_number_docs = request.form['old_number_docs']
        old_company_details = request.form['old_company_details']
        name_company = request.form['name_company']
        number_docs = request.form['number_docs']
        company_details = request.form['company_details']
        if old_name_company != name_company or old_number_docs != number_docs or old_company_details != company_details:
            old_client = Client.query.filter_by(name_company=old_name_company, number_docs=old_number_docs,
                                        company_details=old_company_details).first()
            if old_client:
                db.session.delete(old_client)
                db.session.commit()
            edit_client = Client(id=1, name_company=name_company, number_docs=number_docs, company_details=company_details)
            try:
                db.session.add(edit_client)
                db.session.commit()
            except:
                return 'При зміні клієнта виникла помилка'
            return redirect('/all_client')

@app.route('/user_templates')
def user_templates():
    '''
    doc_file = 'Рахунок.docx'
    doc = Document(doc_file)
    content = []
    for paragraph in doc.paragraphs:
        content.append(paragraph.text)
    '''
    return render_template('user_templates.html')


if __name__ == '__main__':
    app.run(debug=True)
