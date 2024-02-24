from django import forms
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models.functions import Lower
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render

from .forms import BudgetForm, CategoryForm, CategoryRuleForm, DocumentForm, TransactionForm
from .forms import TransactionEditManyForm
from .models import Budget, Category, CategoryRule, Document, Transaction

import csv
from datetime import datetime
from decimal import Decimal
from datetime import date
from decimal import Decimal
import os
import datetime

from django.db.models import Sum
import collections
import random
from random import randint
import string

'''
In this file, you should only see get_object_or_404() for single objects. 
There is no need to wrap it in a try-except block. That’s because get object 
or 404() already does that for you.

Case insensitive/consistent Model ordering
https://docs.djangoproject.com/en/1.10/ref/models/querysets/#order-by

to access files (in document_list)
https://docs.djangoproject.com/en/1.10/topics/files/
d1 = Document.objects.get(id=1)
d1.document.path

upload files (for document_new)
https://simpleisbetterthancomplex.com/tutorial/2016/08/01/how-to-upload-files-with-django.html

Generating a random string.
https://pythontips.com/2013/07/28/generating-a-random-string/
Picking a Random Word In Python?
http://stackoverflow.com/questions/4394145/picking-a-random-word-in-python
'''

def faq(request):
    context = {
        'content_header': 'FAQ, Frequently Asked Questions',
    }
    return render(request, 'beans/faq.html', context)


def about(request):
    '''
    What: Static page informing the visitor of a site summary.
    How: Text to render is passed to the template as part of the context.
    '''
    context = {
        'paragraph1': "One",
        'paragraph2': "Two",
        'paragraph3': "Three",
        'paragraph4': "Four",
        'paragraph5': "Five",
    }
    return render(request, 'beans/about.html', context)


@login_required
def budget_delete(request, pk):
    '''
    What: Deletes a Budget object.
    How: Retrieve a single Budget object from the database by using the "pk"
    parameter in the view invocation. Once we have the Budget object, we
    delete it.
    '''
    budget = get_object_or_404(Budget, pk=pk)
    
    budget.delete()
    return redirect('beans:budget_list')


@login_required
def budget_detail(request, pk):
    '''
    What: Shows all the attributes of a Budget object.
    How: Retrieve a single Budget object from the database by using the "pk"
    parameter in the view invocation. Once we have the Budget object, render
    with a template.
    '''
    budget = get_object_or_404(Budget, pk=pk)
    
    context = {
        'budget': budget
    }
    return render(request, 'beans/budget_detail.html', context)


@login_required
def budget_edit(request, pk):
    '''
    What: Modifies (as Update in CRUD) an existing Budget object.
    
    How: By using a ModelForm and working with the pk of a Budget object 
    passed as part of the request.
    Every time the view is requested the Budget object is retrieved from 
    the database.
    
    The first time the view is requested (HTTP GET verb) the form is presented
    filled with the original attributes of the object. In the case of the 
    Category field, the form also displays categories for which this user does
    not have a Budget.
    
    Once the form fields have been modified, the form is submitted (HTTP POST)
    to this same view and the modified object attributes are saved.
    '''
    budget = get_object_or_404(Budget, pk=pk)
    
    if request.method == "POST":
        form = BudgetForm(request.POST, instance=budget)
        if form.is_valid():
            budget = form.save(commit=False)
            budget.user = request.user
            try:
                budget.save()
            except:
                pass
            return redirect('beans:budget_detail', pk=budget.pk)
    else:
        '''
        First we get the Categories already in use by this user, EXCLUDING the
        Category of the Budget object being edited.
        '''
        categories_budgeted = Budget.objects.filter(
            user=request.user
        ).exclude(
            category=budget.category
        ).values_list(
            'category', flat=True
        )
        
        '''
        To present in the form: Categories for which the user does not have 
        a Budget, AND the Category of the Budget object being edited.
        '''
        categories_to_render = Category.objects.filter(
            user=request.user
        ).exclude(
            id__in=categories_budgeted
        ).order_by(
            Lower('name')
        )
        
        '''
        Pass the list of categories_to_render that we have built to the form.
        '''
        BudgetForm.base_fields['category'] = forms.ModelChoiceField(
            queryset=categories_to_render
        )
        form = BudgetForm(instance=budget)
    
    context = {
        'content_header': 'Edit budget',
        'form': form
    }
    return render(request, 'beans/budget_edit.html', context)


@login_required
def budget_list(request):
    '''
    What: Lists all the Budget objects for the User requesting the view.
    How: Queries the database for a list of all the Budgets, filtering them
    with the User in session, orders them (regardless of their case, and
    renders them.
    '''
    budgets = Budget.objects.filter(
        user=request.user
    ).order_by(Lower('category__name'))
    
    context = {
        'budgets': budgets,
    }
    return render(request, 'beans/budget_list.html', context)


@login_required
def budget_new(request):
    '''
    What: Creates a new Budget object.
    
    How: By using a ModelForm. 
    The first time this view is requested (an HTTP GET verb/method) the form is
    rendered except for the Category field. The Category field presents a list
    of Categories for which this user does not have a Budget.
    
    Once the form is filled, this same view is requested (but in this second
    occassion with an HTTP POST verb/method) and the data of the filled form is
    available in the HTML tags.
    '''
    if request.method == "POST":
        form = BudgetForm(request.POST)
        if form.is_valid():
            budget = form.save(commit=False)
            budget.user = request.user
            try:
                budget.save()
            except:
                '''
                if you try to enter a budget where user/category is not unique
                it throws an error of type IntegrityError, but I do not seem to
                be able to capture it.
                '''
                pass
            return redirect('beans:budget_list')
    else:
        '''
        Only display in in dropdown those Categories for which this user
        does not already have a Budget.
        '''
        '''
        List all the Category ids for which a given user has a Budget.
        Note this a list of ids. Something of the form:
        <QuerySet [10, 14, 23, 6]>
        '''
        categories_budgeted = Budget.objects.filter(
            user=request.user
        ).values_list(
            'category', flat=True
        )
        
        '''
        Category objects for a given user for which there is not a Budget.
        '''
        categoriess_non_budgeted = Category.objects.filter(
            user=request.user
        ).exclude(
            id__in=categories_budgeted
        )
        
        BudgetForm.base_fields['category'] = forms.ModelChoiceField(
            queryset=categoriess_non_budgeted
        )
        form = BudgetForm()
    
    context = {
        'content_header': 'New budget',
        'form': form
    }
    return render(request, 'beans/budget_edit.html', context)


@login_required
def category_delete(request, pk):
    '''
    What: Deletes a Category object. 
    How: Retrieve a single Category object from the database by using the "pk"
    parameter in the view invocation. Once we have the Category object, we 
    delete it.
    '''
    category = get_object_or_404(Category, pk=pk)
    
    try:
        category.delete()
    except:
        pass
    return redirect('beans:category_list')


@login_required
def category_detail(request, pk):
    '''
    What: Shows all the attributes of a Category object.
    How: Retrieve a single Category object from the database by using the "pk"
    parameter in the view invocation. Once we have the Category object, render 
    with a template.
    '''
    category = get_object_or_404(Category, pk=pk)
    
    context = {
        'category': category 
    }
    return render(request, 'beans/category_detail.html', context)


@login_required
def category_edit(request, pk):
    '''
    What: Modifies (as Update in CRUD) an existing Category object.
    
    How: By using a ModelForm and working with the pk of an object. Every time
    the view is requested the Category object is retrieved from the database. 
    
    The first time the view is requested (HTTP GET verb) the form is presented 
    filled with the original attributes of the object.
    
    Once the form fields have been modified, the form is submitted (HTTP POST)
    to this same view and the modified object attributes are saved.
    '''
    category = get_object_or_404(Category, pk=pk)
    
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            return redirect('beans:category_detail', pk=category.pk)
    else:
        form = CategoryForm(instance=category)
    
    context = {
        'content_header': 'Edit category',
        'form': form
    }
    return render(request, 'beans/category_edit.html', context)


@login_required
def category_list(request):
    '''
    What: Lists all the Category objects for the user requesting the view.
    How: Queries the database for a list of all the Categories, filtering them
    with the user in the session, orders them (regardless of their case), and 
    renders them.
    '''
    categories = Category.objects.filter(
        user=request.user
    ).order_by(
        Lower('name')
    )
    
    context = {
        'categories': categories,
    }
    return render(request, 'beans/category_list.html', context)


@login_required
def category_new(request):
    '''
    What: Creates a new Category object.
    
    How: By using a ModelForm.
    The first time this view is requested (an HTTP GET verb/method) the form is
    rendered empty.
    Once the form is filled, this same view is requested (but in this second
    occassion with an HTTP POST verb/method) and the data of the filled form is
    available in the HTML tags.
    '''
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            return redirect('beans:category_list')
    else:
        form = CategoryForm()
    
    context = {
        'content_header': 'New category',
        'form': form
    }
    return render(request, 'beans/category_edit.html', context)


@login_required
def category_rule_delete(request, pk):
    '''
    What: Deletes a CategoryRule object.
    How: Retrieve a single CategoryRule object from the database by using 
    the "pk" parameter in the view invocation. Once we have the
    CategoryRule object, we delete it.
    '''
    category_rule = get_object_or_404(CategoryRule, pk=pk)
    
    category_rule.delete()
    return redirect('beans:category_rule_list')



@login_required
def category_rule_detail(request, pk):
    '''
    What: Shows all the attributes of a CategoryRule object.
    How: Retrieve a single CategoryRule object from the database by using 
    the "pk" parameter in the view invocation. Once we have the 
    CategoryRule object, render with a template.
    '''
    category_rule = get_object_or_404(CategoryRule, pk=pk)
    
    context = {
        'category_rule': category_rule
    }
    return render(request, 'beans/category_rule_detail.html', context)


@login_required
def category_rule_edit(request, pk):
    '''
    What: Modifies (as Update in CRUD) an existing CategoryRule object.
    How: By using a ModelForm and working with the pk of an object. Every time
    the view is requested the CategoryRule object is retrieved from the database.
    The first time the view is requested (HTTP GET verb) the form is presented
    filled with the original attributes of the object. Once the form fields
    have been modified, the form is submitted (HTTP POST) to this same view and
    the modified object attributes are saved.
    In both cases, the full context is passed on to the form (by means of the
    knob 'request=request' when instanstiaing the form.
    '''
    category_rule = get_object_or_404(CategoryRule, pk=pk)
    
    if request.method == "POST":
        form = CategoryRuleForm(request.POST, instance=category_rule, request=request)
        if form.is_valid():
            category_rule = form.save(commit=False)
            # this field, category_rule.user, could be commented
            category_rule.user = request.user
            try:
                category_rule.save()
            except:
                pass
            return redirect('beans:category_rule_detail', pk=category_rule.pk)
    else:
        form = CategoryRuleForm(instance=category_rule, request=request)
    
    context = {
        'content_header': 'Edit category rule',
        'form': form
    }
    return render(request, 'beans/category_rule_edit.html', context)


@login_required
def category_rule_list(request):
    '''
    What: Lists all the CategoryRule objects for the User requesting the view.
    How: Queries the database for a list of all the CategorieRule, filtering 
    them with the User in session, orders them (regardless of their case, and
    renders them.
    '''
    category_rules = CategoryRule.objects.filter(
        user=request.user
    ).order_by(Lower('category__name'))
    
    context = {
        'category_rules': category_rules,
    }
    return render(request, 'beans/category_rule_list.html', context)


@login_required
def category_rule_new(request):
    '''
    What: Creates a new CategoryRule object.
    How: By using a ModelForm. The first time this view is requested (an HTTP
    GET verb/method) the form is rendered empty. Once the form is filled, this
    same view is requested (but in this second occassion with an HTTP POST
    verb/method) and the data of the filled form is available in the HTML tags.
    In both cases, the full context is passed on to the form (by means of the 
    knob 'request=request' when instanstiaing the form.
    '''
    if request.method == "POST":
        form = CategoryRuleForm(request.POST, request=request)
        if form.is_valid():
            category_rule = form.save(commit=False)
            category_rule.user = request.user
            try:
                category_rule.save()
            except:
                pass
            return redirect('beans:category_rule_list')
    else:
        form = CategoryRuleForm(request=request)
    
    context = {
        'content_header': 'New category rule',
        'form': form
    }
    return render(request, 'beans/category_rule_edit.html', context)


@login_required
def document_delete(request, pk):
    '''
    What: Deletes a Document object.
    
    How: Retrieve a single Document object from the database by using the "pk"
    parameter in the view invocation. Once we have the Document object, we
    delete it.
    First we delete the file from the filesystem, then we delete the object
    from the database.
    '''
    doc = get_object_or_404(Document, pk=pk)
    
    try:
        '''
        Wouldn't it be great if this could be made into a transaction? The two
        commands in one single atomic operation?
        '''
        os.remove(doc.document.path)
        doc.delete()
    except:
        pass
    return redirect('beans:document_list')


def document_import(request, document_id):
    '''
    What: Creates a number of Transaction objects by importing the contents 
    of a CSV file into the database. For each line in the CSV file, one
    Transaction record is created.
    How: Retrieve a (1, one) Document object from the database by using the
    "pk" parameter in the view invocation. From the Document object we can 
    figure the path within the filesystem and operate directly on the file. 
    Note that the code does not validate whether the file is a CSV file or not.
    The code expects the file to have a certain format. 
    '''
    doc = Document.objects.get(pk=document_id)
    
    file_path = doc.document.path
    with open(file_path) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            t = Transaction()
            
            t.date = row[' Posted Transactions Date']
            t.date = datetime.strptime(t.date, "%d/%m/%Y")
            
            t.description = row[' Description1']
            
            # let's do the amount
            # pluck the value under the ' Debit Amount' key
            # sanitize and convert to a Decimal figure
            a = row[' Debit Amount']
            a = a.replace(',', '')
            a = Decimal(a)
            t.amount = a
            
            t.category = Category.objects.get(pk=43)
            t.user = request.user
            t.save()
            #print("produce log output to verify", t.date)
            #print(t.category)
            #print(t.user)
    return redirect('beans:transaction_list')


def document_list(request):
    '''
    What: Lists all the Document objects for the User requesting the view.
    How: Queries the database for a list of all the Documents, filtering them
    with the User in session, and renders them.
    '''
    documents = Document.objects.filter(
        user=request.user
    )
    
    context = {
        'documents': documents,
    }
    return render(request, 'beans/document_list.html', context)


def document_new(request):
    '''
    What: Creates a new Document object.
    How: By using a ModelForm. The first time this view is requested (an HTTP
    GET verb/method) the form is rendered empty. Once the form is filled, this
    same view is requested (but in this second occassion with an HTTP POST
    verb/method) and the data of the filled form is available in the HTML tags.
    '''
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.user = request.user
            try:
                document.save()
            except:
                pass
            return redirect('beans:document_list')
    else:
        form = DocumentForm()
    
    context = {
        'form': form,
    }
    return render(request, 'beans/document_new.html', context)


@login_required
def report_month(request):
    if request.method == 'POST':
        if request.POST.get('report_date'):
            d = request.POST.get('report_date')
            d = datetime.datetime.strptime(d, "%Y-%m-%d")
        else:
            d = datetime.date.today()
    else:
        d = datetime.date.today()
    
    # build dictionary where the keys are the categories and the values the sum
    # of all the transactions in that category
    # https://pymotw.com/2/collections/ordereddict.html
    dict_expense_budget = collections.OrderedDict()
    
    categories = Category.objects.all()
    categories = Category.objects.filter(
        user=request.user
    ).order_by(Lower('name'))
    #print(categories)
    for cat in categories:
        # figure all the transactions for the user, category and month
        t = Transaction.objects.filter(
            category__name=cat.name,
            user=request.user,
            date__year=d.year,
            date__month=d.month
        )
        # sum all the transactions for the user, category and month
        t_sum = t.aggregate(Sum('amount'))
        t_sum = t_sum['amount__sum']
        if t_sum is None:
            t_sum =0
        
        
        # figure what is the budget for a given user and category
        b = Budget.objects.filter(
            category__name=cat.name,
            user=request.user
        )
        # sum all the budget for a given user and category
        # necessary due to how django operates
        b_sum = b.aggregate(Sum('amount'))
        b_sum = b_sum['amount__sum']
        if b_sum is None:
            b_sum =0
        
        # figure what is the difference between the budget and the expenditure
        delta = b_sum - t_sum
        
        # put in a list: expenditure, budget, delta
        l = []
        l.append(t_sum)
        l.append(b_sum)
        l.append(delta)
        
        # populate the dictionary to be rendered
        dict_expense_budget[cat.name] = l
    
    context = {
        'expense_vs_budget': dict_expense_budget,
        'report_date': d,
    }
    #print("This should be in order")
    #print(dict_expense_budget)
    return render(request, 'beans/report_month.html', context)


@login_required
def report_year(request):
    if request.method == 'POST':
        if request.POST.get('report_date'):
            d = request.POST.get('report_date')
            d = datetime.datetime.strptime(d, "%Y-%m-%d")
        else:
            d = datetime.date.today()
    else:
        d = datetime.date.today()
    
    # build dictionary where the keys are the categories and the values the sum
    # of all the transactions in that category
    # https://pymotw.com/2/collections/ordereddict.html
    dict_expense_budget = collections.OrderedDict()
    
    categories = Category.objects.all()
    categories = Category.objects.filter(
        user=request.user
    ).order_by(Lower('name'))
    #print(categories)
    for cat in categories:
        # figure all the transactions for the user, category and year
        t = Transaction.objects.filter(
            category__name=cat.name,
            user=request.user,
            date__year=d.year
            #date__month=d.month
        )
        # sum all the transactions for the user, category and month
        t_sum = t.aggregate(Sum('amount'))
        t_sum = t_sum['amount__sum']
        if t_sum is None:
            t_sum =0
        
        
        # figure what is the budget for a given user and category
        b = Budget.objects.filter(
            category__name=cat.name,
            user=request.user
        )
        # sum all the budget for a given user and category
        # necessary due to how django operates
        b_sum = b.aggregate(Sum('amount'))
        b_sum = b_sum['amount__sum']
        if b_sum is None:
            b_sum =0
        
        b_sum = b_sum * 12
        
        # figure what is the difference between the budget and the expenditure
        delta = b_sum - t_sum
        
        # put in a list: expenditure, budget, delta
        l = []
        l.append(t_sum)
        l.append(b_sum)
        l.append(delta)
        
        # populate the dictionary to be rendered
        dict_expense_budget[cat.name] = l
        
    context = {
        'expense_vs_budget': dict_expense_budget,
        'report_date': d,
    }
    #print("This should be in order")
    #print(dict_expense_budget)
    return render(request, 'beans/report_year.html', context)


def set_user_initial_data(request):
    seed_category_rules = CategoryRule.objects.filter(user__username='seed_user')
    #print(seed_category_rules)
    for seed_category_rule in seed_category_rules:
        #print(seed_category_rule.category)
        #print(seed_category_rule.keyword)

        ''' create Categories using the seed file'''
        category = Category()
        category.name = seed_category_rule.category.name
        category.user = request.user
        #print(category.name)
        try:
            category.save()
        except:
            #print('Could not save the Category, maybe already exists?')
            pass

        ''' create Budgets, use the categories we have just created '''
        budget = Budget()
        budget.amount = round(random.uniform(30, 40), 0)
        budget.category = Category.objects.get(name=category.name, user=request.user)
        budget.user = request.user
        try:
            budget.save()
        except:
            #print('Could not save the Budget, maybe already exists?')
            pass

        '''
        create CategoryRule, use the keywords in the seed file and the
        categories we have just created
        '''
        category_rule = CategoryRule()
        category_rule.category = Category.objects.get(name=category.name, user=request.user)
        category_rule.keyword = seed_category_rule.keyword
        category_rule.user = request.user
        try:
            category_rule.save()
        except:
            #print('Could not save the CategoryRule, maybe already exists?')
            pass

    ''' create Transactions
    We leave the Category field empty, this will force the user to
    clasify the transaction.
    The transaction.description field is a psudorandom string containing
    at least one of the keywords we have just created in the CategoryRule.
    '''
    for i in range(CategoryRule.objects.filter(user=request.user).count()):
        transaction = Transaction()
        transaction.amount = round(random.uniform(10, 110), 2)
        transaction.date = date.today() - datetime.timedelta(365*2 + randint(-16, 16))

        random_category_rule = random.choice(CategoryRule.objects.filter(user=request.user))

        transaction.category = random_category_rule.category

        random_keyword = random_category_rule.keyword
        random_prefix = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(randint(3, 8))])
        random_suffix = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(randint(2, 9))])
        transaction.description = random_prefix + random_keyword + random_suffix

        transaction.user = request.user
        try:
            transaction.save()
        except:
            pass

    return redirect('beans:about')


def transaction_auto_classify(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    #print(transaction.description.lower())
    #print(type(transaction.description.lower()))
    category_rules = CategoryRule.objects.filter(user=request.user)
    for category_rule in category_rules:
        #print(transaction.description.lower())
        #print(category_rule.keyword.lower())
        #print(type(category_rule.keyword.lower()))
        #print(category_rule.keyword.lower() in transaction.description.lower())
        if category_rule.keyword.lower() in transaction.description.lower():
            transaction.category = category_rule.category
        else:
            #transaction.category = Category.objects.get(name='Uncategorized')
            pass
        transaction.save()
    return redirect('beans:transaction_list')


@login_required
def transaction_delete(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    transaction.delete()
    return redirect('beans:transaction_list')


@login_required
def transaction_detail(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    context = {
        'transaction': transaction
    }
    return render(request, 'beans/transaction_detail.html', context)


@login_required
def transaction_edit(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    if request.method == "POST":
        form = TransactionForm(request.POST, instance=transaction, request=request)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return redirect('beans:transaction_list')
    else:
        form = TransactionForm(instance=transaction, request=request)

    context = {
        'content_header': 'Edit transaction',
        'form': form
    }
    return render(request, 'beans/transaction_edit.html', context)


def transaction_edit_many(request):
    '''
    This view is a confirmation page before modifying the objects.
    This view does NOT modify objects, DOES show objects and pass them to
    another view: transaction_update_many. What this view passes are in fact
    the object ID, not the objects themselves. The object ID are passed as
    part of the HTML POST message. The ID are scraped from checkbox HTML tags
    in the template.
    '''
    transaction_ids_to_edit = request.POST.getlist('checked_transaction')

    '''
    convert to objects. Only reason for this is is so that the objects can
    be shown to the user in the template
    '''
    # can this query throw an error? modify to try/except?
    transaction_objects_to_edit = Transaction.objects.filter(pk__in=transaction_ids_to_edit)

    ''' put in a form '''
    #form = TransactionForm()

    ''' test '''
    formTransactionEditManyForm = TransactionEditManyForm(user=request.user)

    context = {
        'transaction_ids_to_edit': transaction_ids_to_edit,
        'transaction_objects_to_edit': transaction_objects_to_edit,
        #'form': form,
        'formTransactionEditManyForm': formTransactionEditManyForm,
        'paragraph1': transaction_ids_to_edit,
        'paragraph2': "Second step",
        'paragraph3': "Third step",
    }
    return render(request, 'beans/transaction_edit_many.html', context)


def transaction_update_many(request):
    '''
    This view does modify objects. The objects do come on the HTML POST message
    from another view, transaction_edit_many. There is no template associated
    to this view. Once the objects have been modified, it redirects.
    '''
    transaction_ids_to_update = request.POST.getlist('checked_transaction')
    transactions_to_update = Transaction.objects.filter(id__in=transaction_ids_to_update)

    date = request.POST.get('date')
    if date != "":
        transactions_to_update.update(date=date)

    description = request.POST.get('description')
    if description != "":
        transactions_to_update.update(description=description)

    amount = request.POST.get('amount')
    try:
        if isinstance(Decimal(amount), Decimal):
            transactions_to_update.update(amount=amount)
    except:
        pass

    category = request.POST.get('category')
    try:
        if int(category) != 0:
            transactions_to_update.update(category=category)
    except:
        pass

    context = {
        'transaction_ids_to_edit': transaction_ids_to_update,
        'date': date,
        'description': description,
        'amount': amount,
        'category': category,
        'paragraph1': "First step",
        'paragraph2': "Second step",
        'paragraph3': "Third step",
    }
    #return render(request, 'beans/transaction_update_many.html', context)
    return redirect('beans:transaction_list')



@login_required
def transaction_list(request):
    transaction_list = Transaction.objects.filter(
        user=request.user
    ).order_by('date')

    # pagination
    # https://simpleisbetterthancomplex.com/tutorial/2016/08/03/how-to-paginate-with-django.html
    page = request.GET.get('page', 1)

    paginator = Paginator(transaction_list, 666)
    try:
        transactions = paginator.page(page)
    except PageNotAnInteger:
        transactions = paginator.page(1)
    except EmptyPage:
        transactions = paginator.page(paginator.num_pages)

    context = {
        'transactions': transactions,
    }
    return render(request, 'beans/transaction_list.html', context)


@login_required
def transaction_new(request):
    if request.method == "POST":
        form = TransactionForm(request.POST, request=request)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return redirect('beans:transaction_list')
    else:
        form = TransactionForm(request=request)
    context = {
        'content_header': 'New transaction',
        'form': form
    }
    return render(request, 'beans/transaction_edit.html', context)
