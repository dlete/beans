# execute with
# python manage.py shell < scrap_ag.py

# standard Django, import the models we need
from beans.models import Category, Vendor, Transaction

# need this to calculate sums 
from django.db.models import Sum

# warming up
categories = Category.objects.all()
transactions = Transaction.objects.all()

# sum all the transactions
s = Transaction.objects.all().aggregate(Sum('amount'))
# select all transactions that are of a given category
t = Transaction.objects.filter(category__name='Housecare')

dict = {}
for c in categories:
    cat_name = c.name
    t = Transaction.objects.filter(category__name=cat_name)
    t_sum = t.aggregate(Sum('amount'))
    print(cat_name, t_sum, t_sum['amount__sum'])
    dict[cat_name] = t_sum['amount__sum']

dict

for d in dict:
    print(d, dict[d])

