from docx import Document
from docx2pdf import convert
from datetime import datetime
from num2words import num2words
import pythoncom
import pathlib

def replace_text(doc, old_text, new_text):#функция заменяющая текст в файле
    for paragraph in doc.paragraphs:
        if old_text in paragraph.text:
            paragraph.text = paragraph.text.replace(old_text, new_text)

        for run in paragraph.runs:
            if old_text in run.text:
                run.text = run.text.replace(old_text, new_text)

    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    if old_text in paragraph.text:
                        paragraph.text = paragraph.text.replace(old_text, new_text)

                    for run in paragraph.runs:
                        if old_text in run.text:
                            run.text = run.text.replace(old_text, new_text)


def make_doc(name_templates, name_company, number_doc, company_details, money):
    path_to_doc = f'static/docs_template/{name_templates}.docx'
    doc = Document(path_to_doc)
    replace_text(doc, 'КОМПАНІЯ', name_company)
    replace_text(doc, 'НОМЕР_ДОГОВОРУ', number_doc)
    replace_text(doc, 'РЕКВІЗИТИ_КОМПАНІЇ', company_details)
    replace_text(doc, 'СУММА', money)
    replace_text(doc, 'ПРОПИСОМ', num2words(int(money), lang='uk'))
    replace_text(doc, 'ДАТА', f'{datetime.today().day}.{datetime.today().month}.{datetime.today().year}')
    replace_text(doc, 'МІСЯЦЬ', f'{datetime.today().month}')
    replace_text(doc, 'РІК', f'{datetime.today().year}'[2:])
    doc.save('static/docs_template/chenge.docx')


def doc_to_pdf():
    pythoncom.CoInitialize()
    convert("static/docs_template/chenge.docx", "static/chenge.pdf")

def doc_to_pdf_new(name):
    pythoncom.CoInitialize()
    convert(f"static/docs_template/{name}.docx", f"static/{name}.pdf")

def all_files(): #просматриваем все файлы в директории
    files =[]
    currentDirectory = pathlib.Path('./static/docs_template')
    for currentFile in currentDirectory.iterdir():
        files.append(currentFile.name)
    return files





'''
gen_name = 'ТОВ "МАМОНТ-АГРО"'
gen_number = '387550443'
gen_detail = 'ТОВАРИСТВО З ОБМЕЖЕНОЮ ВІДПОВІДАЛЬНІСТЮ "МАМОНТ-АГРО"\n' \
             'Адреса: 02095, Україна, м. Київ, вул. Княжий Затон 21, прим. 566, 576\n' \
             'Код ЄДРПОУ: 41947062\n' \
             'ІПН: 419470626515\n' \
             'IBAN: UA023808050000000026009597181\n' \
             'У банку АТ «Райффайзен Банк Аваль»\n' \
             '\n\n\nДиректор Роман Бундін'
gen_money = '3500'
'''

#make_doc('Приклад_1', gen_name, gen_number, gen_detail, gen_money)
#print(num2words('455.33', lang='uk'))