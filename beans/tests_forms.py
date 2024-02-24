from django.test import TestCase

from beans.models import Budget, Category
from beans.forms import BudgetForm


class Budget_Form_Test(TestCase):
    ''' 
    the form BudgetForm has the fields: amount and category
    it is not necessary though to test the user component of the Budget model
    '''
    def setUp(self):
        category_name = 'testcategory'
        category = Category.objects.create(name=category_name)

    # Valid Form
    def test_BudgetForm_valid(self):
        # Form unit test with Foreign Key
        # http://stackoverflow.com/questions/34317847/django-forms-unit-tests-with-foreignkey
        data = {
            'amount': 33,
            'category': Category.objects.get(id=1).pk
        }
        form = BudgetForm(data)
        self.assertTrue(form.is_valid())

    # Invalid Amount type
    def test_BudgetForm_invalid(self): 
        data = {
            'amount': "thirtythree",
            'category': Category.objects.get(id=1).pk
        }
        form = BudgetForm(data)
        self.assertFalse(form.is_valid())

    # Invalid Category
    # PENDING

    # Invalid User
    # n/a, the form BudgetForm does not have a User field

    # Empty Amount
    def test_BudgetForm_empty_amount(self):
        data = {
            'amount': '',
            'category': Category.objects.get(id=1).pk
        }
        form = BudgetForm(data)
        self.assertFalse(form.is_valid())

    # Empty Category
    def test_BudgetForm_empty_category(self):
        data = {
            'amount': 33,
            'category': ''
        }
        form = BudgetForm(data)
        self.assertFalse(form.is_valid())

    # Empty User 
    # n/a, the form BudgetForm does not have a User field


from beans.models import Category
from beans.forms import CategoryForm

class Category_Form_Test(TestCase):
    # Valid Form
    def test_CategoryForm_valid(self):
        data = {
            'name': 'testcategory'
        }
        form = CategoryForm(data)
        self.assertTrue(form.is_valid())

    # Empty Name
    def test_CategoryForm_empty_name(self):
        data = {
            'name': ''
        }
        form = CategoryForm(data)
        self.assertFalse(form.is_valid())


'''
from beans.models import Document
from beans.forms import DocumentForm
from django.core.files.uploadedfile import SimpleUploadedFile

class Document_Form_Test(TestCase):
    def setUp(self):
        file_path = '/workspace/pjt_beans/mysite/beans/tests_forms.py'

    def test_DocumentForm_valid(self):
        upload_file = open('/workspace/pjt_beans/mysite/beans/tests_forms.py', 'rb')
        data = {
            'description': 'testdocument',
            'document': SimpleUploadedFile(upload_file.name, upload_file.read())
        }
        form = DocumentForm(data)
        self.assertTrue(form.is_valid())
'''

from beans.models import Transaction
from beans.forms import TransactionForm
import datetime

class Transaction_Form_Test(TestCase):
    '''
    the form TransactionForm has the fields: date, description, amount and category
    it is not necessary though to test the user component of the Budget model
    '''
    def setUp(self):
        category_name = 'testcategory'
        category = Category.objects.create(name=category_name)

	# Valid Form
    def test_TransactionForm_valid(self):
        data = {
            'amount': 33,
            'category': Category.objects.get(id=1).pk,
            'date': datetime.date.today(),
            'description': 'testdescription'
        }
        form = TransactionForm(data)
        self.assertTrue(form.is_valid())

    # Invalid Amount type
    def test_TransactionForm_invalid_amount(self):
        data = {
            'amount': 'thirtythree',
            'category': Category.objects.get(id=1).pk,
            'date': datetime.date.today(),
            'description': 'testdescription'
        }
        form = TransactionForm(data)
        self.assertFalse(form.is_valid())

    # Invalid Date type
    def test_TransactionForm_invalid_date(self):
        data = {
            'amount': 33,
            'category': Category.objects.get(id=1).pk,
            'date': 'todayintext',
            'description': 'testdescription'
        }
        form = TransactionForm(data)
        self.assertFalse(form.is_valid())

    # Invalid Description type
    # n/a, because since the field is text, it will accept anything

    # Invalid Category type
    # n/a, because it is a dropdown feed from Foreign Key

    # Empty Amount
    def test_TransactionForm_empty_amount(self):
        data = {
            'amount': '',
            'category': Category.objects.get(id=1).pk,
            'date': datetime.date.today(),
            'description': 'testdescription'
        }
        form = TransactionForm(data)
        self.assertFalse(form.is_valid())

    # Empty Category
    def test_TransactionForm_empty_category(self):
        data = {
            'amount': 33,
            'category': '',
            'date': datetime.date.today(),
            'description': 'testdescription'
        }
        form = TransactionForm(data)
        self.assertFalse(form.is_valid())

    # Empty Date
    def test_TransactionForm_empty_date(self):
        data = {
            'amount': '33',
            'category': Category.objects.get(id=1).pk,
            'date': '',
            'description': 'testdescription'
        }
        form = TransactionForm(data)
        self.assertFalse(form.is_valid())

    # Empty Description
    def test_TransactionForm_empty_description(self):
        data = {
            'amount': '33',
            'category': Category.objects.get(id=1).pk,
            'date': datetime.date.today(),
            'description': ''
        }
        form = TransactionForm(data)
        self.assertFalse(form.is_valid())

