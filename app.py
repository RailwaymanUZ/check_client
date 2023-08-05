from flask import Flask, render_template, url_for, request, redirect, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_login.mixins import UserMixin
from flask_sqlalchemy import SQLAlchemy

from db import value_to_db

import base64

from functions import make_doc, doc_to_pdf, doc_to_pdf_new, all_files, delete_files, delete_generation_files, make_doc_standart, doc_to_pdf_standart


# переместить эту функцию после того как всё будет работать для нормальной структуры приложения
def save_pdf_to_db(id, name, content_pdf):
    user_temp = Document.query.filter_by(id=id, name=name).first()
    user_temp.format_pdf = content_pdf
    db.session.add(user_temp)
    db.session.commit()

def b64encode_filter(data):
    if data is None:
        return ''
    return base64.b64encode(data).decode('utf-8')






app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///client.db'
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
app.secret_key = 'jpiodfujgoisdufg-098ui-09poj;ildskfg'
app.jinja_env.filters['b64encode'] = b64encode_filter


class Client(db.Model):
    id = db.Column(db.Integer, primary_key=False)
    name_company = db.Column(db.String(100), primary_key=True, nullable=False)
    number_docs = db.Column(db.String(100), primary_key=True)
    adress = db.Column(db.Text)
    edrpou = db.Column(db.Integer)
    ipn = db.Column(db.String(50))
    iban = db.Column(db.String(100))
    tel = db.Column(db.String(100))
    email = db.Column(db.String(50))
    other_data = db.Column(db.Text)
    director = db.Column(db.String(50))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    login = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(250), nullable=False)

class Document(db.Model):
    id_doc = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.Integer)
    name = db.Column(db.String(100))
    format_docx = db.Column(db.LargeBinary)
    format_pdf = db.Column(db.LargeBinary)

#    def __repr__(self):
#        return '<Client &r>' % self.id



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route('/')
def index():
    return render_template('index.html',current_user=current_user)

@app.route('/faqs')
def faqs():
    return render_template('faqs.html')


@app.route('/add_client', methods=['POST', 'GET'])
@login_required
def add_client():
    if request.method == 'POST':
        name_company = request.form['name_company']
        if value_to_db(name_company) != True:
            return render_template('error_page.html')

        number_doc = request.form['number_docs']
        if value_to_db(number_doc) != True:
            return render_template('error_page.html')

        adress = request.form['adress']
        edrpou = request.form['edrpou']
        ipn = request.form['ipn']
        iban = request.form['iban']
        tel = request.form['tel']
        email = request.form['email']
        other_data = request.form['other_data']
        director = request.form['director']
        # делаем запись в бд
        client = Client(id=current_user.id,name_company=name_company, number_docs=number_doc, adress=adress, edrpou=edrpou,
                        ipn=ipn, iban=iban, tel=tel, email=email, other_data=other_data, director=director)
        try:
            db.session.add(client)
            db.session.commit()
            return redirect('/all_client') # перенаправляем на станичку
        except:
            return 'При додаванні клієнта виникла помилка'

    else:
        return render_template('add_client.html')

@app.route('/all_client')
@login_required
def all_client():
    user_id = current_user.id
    client = Client.query.filter_by(id=user_id).all()
    return render_template('all_client.html', client=client)

@app.route('/delete_client', methods=['POST'])
@login_required
def delete_client():
    name_company = request.form['name_company']
    number_docs = request.form['number_docs']
    del_client = Client.query.filter_by(id=current_user.id, name_company=name_company, number_docs=number_docs,).first()
    if del_client:
        db.session.delete(del_client)
        db.session.commit()

    return redirect('/all_client')


@app.route('/edit_client', methods=['POST'])
@login_required
def edit_client():
    hiden_information = request.form['hiden_information']
    if hiden_information == 'first_vision':
        name_company = request.form['name_company']
        number_docs = request.form['number_docs']
        adress = request.form['adress']
        edrpou = request.form['edrpou']
        ipn = request.form['ipn']
        iban = request.form['iban']
        tel = request.form['tel']
        email = request.form['email']
        other_data = request.form['other_data']
        director = request.form['director']

        old_client = Client(id=current_user.id,name_company=name_company, number_docs=number_docs, adress=adress, edrpou=edrpou,
                        ipn=ipn, iban=iban, tel=tel, email=email, other_data=other_data, director=director)

        return render_template('edit_client.html', old_client=old_client)

    if hiden_information == 'chenge':
        # выбираем старые значения
        old_name_company = request.form['old_name_company']
        old_number_docs = request.form['old_number_docs']
        old_adress = request.form['old_adress']
        old_edrpou = request.form['old_edrpou']
        old_ipn = request.form['old_ipn']
        old_iban = request.form['old_iban']
        old_tel = request.form['old_tel']
        old_email = request.form['old_email']
        old_other_data = request.form['old_other_data']
        old_director = request.form['old_director']
        #d выбираем новые значения
        name_company = request.form['name_company']
        number_docs = request.form['number_docs']
        adress = request.form['adress']
        edrpou = request.form['edrpou']
        ipn = request.form['ipn']
        iban = request.form['iban']
        tel = request.form['tel']
        email = request.form['email']
        other_data = request.form['other_data']
        director = request.form['director']
        # проверяем, есть ли изменения
        if old_name_company != name_company or old_number_docs != number_docs or old_adress != adress\
                or old_edrpou != edrpou or old_ipn != ipn or old_iban != iban or old_tel != tel or old_email != email\
                or old_other_data != other_data or old_director != director:
            old_client = Client.query.filter_by(id=current_user.id, name_company=old_name_company, number_docs=old_number_docs).first()
            if old_client:
                db.session.delete(old_client)
                db.session.commit()
            edit_client = Client(id=current_user.id,name_company=name_company, number_docs=number_docs, adress=adress, edrpou=edrpou,
                        ipn=ipn, iban=iban, tel=tel, email=email, other_data=other_data, director=director)
            try:
                db.session.add(edit_client)
                db.session.commit()
            except:
                return 'При зміні клієнта виникла помилка'
            return redirect('/all_client')

@app.route('/user_templates', methods=['POST', 'GET'])
@login_required
def user_templates():
    if request.method == 'POST' and ('Приклад_1' in request.form['doc'] or 'Приклад_2' in request.form['doc']):
        gen_name_doc = request.form['doc']
        gen_client = request.form['name_company']
        if request.form['money'] != '':
            gen_money = request.form['money']
        else:
            gen_money = ''
        client = Client.query.filter_by(id=current_user.id, name_company=gen_client).first()
        make_doc_standart(gen_name_doc, client.name_company, client.number_docs, client.company_details, gen_money)
        doc_to_pdf_standart()
        return render_template('redy_standart_template.html')
    if request.method == 'POST' and 'delete' in request.form:
        name_doc = request.form['doc']
        delete_doc = Document.query.filter_by(id=current_user.id, name=name_doc).first()
        db.session.delete(delete_doc)
        db.session.commit()
        return redirect('/user_templates')
    if request.method == "POST":
        # получаем данные от пользователя с шаблоном и номером документа для генерации
        gen_client = request.form['name_company']
        gen_doc = request.form['doc']
        # проверяем указали ли сумму
        if request.form['money'] != '':
            gen_money = request.form['money']
        else:
            gen_money = ''
        # выбираем данные из database Клиентов
        client = Client.query.filter_by(id=current_user.id, name_company=gen_client).first()
        gen_name = client.name_company
        gen_number = client.number_docs
        gen_adress = client.adress
        gen_edrpou = client.edrpou
        gen_ipn = client.ipn
        gen_iban = client.iban
        gen_tel = client.tel
        gen_email = client.email
        gen_other_data = client.other_data
        gen_director = client.director
        # выбираем данные из database Документов
        document = Document.query.filter(Document.id==current_user.id, Document.name==gen_doc).first()
        # вытягиваем файл из бд в статик с именем пользователя
        with open(f'static/docs_template/{current_user.id}.docx', 'wb') as file:
            file.write(document.format_docx)
        # формируем docx документ
        make_doc(current_user.id, gen_name, gen_number, gen_adress, gen_edrpou, gen_ipn, gen_iban, gen_tel, gen_email,
                 gen_other_data, gen_director, gen_money)
        # формируем pdf документ
        doc_to_pdf(current_user.id)
        return render_template('redy_template.html', name_file=str(current_user.id))
    else:
        #Выбираем всех клиентов
        client = Client.query.filter(Client.id == current_user.id).all()
        files = Document.query.filter(Document.id == current_user.id).all()
        # обратить внимание на шаблон и грамотно его отредактировать !!!!!!!!
        return render_template('user_templates.html', client=client, files=files)

@app.route('/upload', methods=['POST', 'GET'])
@login_required
def upload():
    name_new_file = request.form['name_new_file']
    file = request.files['new_file']
    # переводим файл в бинарный код
    content_doc = file.read()
    # проверяем добавлялся ли файл в загрузку
    if len(content_doc) == 0:
        flash('Необхідно завантажити файл')
        return redirect('/user_templates')
    # сохраняем файл для его конвертации в pdf - name = id
    with open(f'{current_user.id}.docx', 'wb') as docx_file:
        docx_file.write(content_doc)
    # cохраняем файл формата pdf
    doc_to_pdf_new(current_user.id)
    # сохраем имя и файл docx в бд
    doc_doc = Document(id=current_user.id, name=name_new_file, format_docx=content_doc)
    db.session.add(doc_doc)
    db.session.commit()
    # сохраняем файл в формате pdf в БД
    with open(f'{current_user.id}.pdf', 'rb') as pdf_file:
        content_pdf = pdf_file.read()
    save_pdf_to_db(current_user.id, name_new_file, content_pdf)
    #удаляем файлы который созадвались для переноса в бд
    delete_generation_files(current_user.id)
    return redirect('/user_templates')

@app.route('/login', methods=['POST', 'GET'])
def login():
    log_user = request.form['login']
    password_user = request.form['password']
    if log_user and password_user and User.query.filter_by(login=log_user).first() != None:
        user = User.query.filter_by(login=log_user).first()
        if password_user == user.password:
            login_user(user)
            return redirect('/user_templates')
        else:
            flash('Вибачте, але логін та пароль не дійсні')
    else:
        flash('Будь ласка авторизуйтесь')
        return render_template('index.html')

@app.route('/logout', methods=['POST', 'GET'])
@login_required
def logout():
    logout_user()
    return redirect('/')

@app.after_request
def refirect_to_index(response):
    if response.status_code == 401:
        return redirect('/')
    return response


if __name__ == '__main__':
    app.run(debug=True)
