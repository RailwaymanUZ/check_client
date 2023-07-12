from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from db import value_to_db
from functions import make_doc, doc_to_pdf, doc_to_pdf_new, all_files


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
            return redirect('/all_client') # перенаправляем на станичку
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

@app.route('/user_templates', methods=['POST', 'GET'])
def user_templates():
    if request.method == "POST":
        # получаем данные от пользователя с шаблоном и номером документа для генерации
        gen_client = request.form['name_company']
        gen_doc = request.form['doc']
        gen_money = request.form['money']
        # выбираем данные из database
        client = Client.query.filter_by(name_company=gen_client).first()
        gen_name = client.name_company
        gen_number = client.number_docs
        gen_detail = client.company_details
        # формируем docx документ
        make_doc(gen_doc, gen_name, gen_number, gen_detail, gen_money)
        # формируем pdf документ
        doc_to_pdf()

        return render_template('redy_template.html')
    else:
        #Выбираем всех клиентов
        client = Client.query.all()
        files = all_files()
        return render_template('user_templates.html', client=client, files=files)

@app.route('/upload', methods=['POST', 'GET'])
def upload():
    name_new_file = request.form['name_new_file']
    file = request.files['new_file']
    file.save(f'static/docs_template/{name_new_file}.docx')
    doc_to_pdf_new(name_new_file)
    return redirect('/user_templates')

if __name__ == '__main__':
    app.run(debug=True)
