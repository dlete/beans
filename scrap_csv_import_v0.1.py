# execute with
# python manage.py shell < <this_file.py>


# standard Django, import the models we need
from beans.models import Document

import csv

with open('Transaction_Export_01.10.2016_22.20.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        #print(row)
        print(row[' Posted Transactions Date'])
        print(row[' Description1'])
        print(row[' Debit Amount'])
        #for key, value in row.items():
        #    print(key, value)


with open('Transaction_Export_01.10.2016_22.20.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        print(row[' Posted Transactions Date'])
        print(row[' Description1'])
        print(row[' Debit Amount'])
#        print(row)
#        for key, value in row.items():
#            print(key, value)

