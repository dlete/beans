# execute with
# python manage.py shell < <this_file.py>


# standard Django, import the models we need
from beans.models import Document, Transaction

import csv

d = Document.objects.get(pk=5)
d.document.name
d.document.path

csv_file = d.document.path

#with open('/workspace/pjt_beans/mysite/media/documents/Transaction_Export_01.10.2016_22.20.csv') as csvfile:
with open(csv_file) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        d = Document()
        d.date = row[' Posted Transactions Date']
        d.description = row[' Description1']
        d.amount = row[' Debit Amount']
        print(d.date)
        #print(row)
        #print(row[' Posted Transactions Date'])
        #print(row[' Description1'])
        #print(row[' Debit Amount'])
        #for key, value in row.items():
        #    print(key, value)


def document_import(document_id):
    doc = Document.objects.get(pk=document_id)
    file_path = doc.document.path
    with open(file_path) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            t = Transaction()
            t.date = row[' Posted Transactions Date']
            # tell me what type of object t.date is, should be string
            print("this is what type of object is date", type(t.date))
            # convert to Date
            from datetime import datetime
            d = datetime.strptime(t.date, "%d/%m/%Y")
            print("type of converted date", type(d))
            t.description = row[' Description1']
            t.amount = row[' Debit Amount']
            # tell me what type of object t.amount is, should be string
            print("this is what type of object is amount", type(t.amount))
            # converto to Decimal
            from decimal import Decimal
            a = t.amount
            a = a.replace(',', '')
            a = Decimal(a)
            print(a)
            #a = Decimal(a.replace(',', ''()))
            #a = float(a.strip)
            print("type of converted amount", type(a))


document_import(5)
