from django.test import TestCase

# Create your tests here.
#https://realpython.com/blog/python/testing-in-django-part-1-best-practices-and-examples/

# models test
from django.contrib.auth.models import *
from beans.models import Budget
from beans.models import Category

class BudgetTest(TestCase):

    def create_budget(self, user=User.objects.get(id=1), category=Category.objects.get(id=1), amount="33.3"):
        return Budget.objects.create(user=user, category=category, amount=amount)

    def test_budget_creation(self):
        b = self.create_budget()
        self.assertTrue(isinstance(b, Budget))
        self.assertEqual(b.__str__(), b.category.name)


class CategoryTest(TestCase):

    def create_category(self, name="test category name"):
        return Category.objects.create(name=name)

    def test_category_creation(self):
        c = self.create_category()
        self.assertTrue(isinstance(c, Category))
        self.assertEqual(c.__str__(), c.name)


from beans.models import Transaction
import datetime
from django.contrib.auth.models import *
class TransactionTest(TestCase):

    #bogus_category = Category.objects.get(id=1)
    #user = User.objects.get(id=1)

    def create_transaction(self, user=User.objects.get(id=1), date=datetime.date.today(), description="test transaction description", amount="33.3", category=Category.objects.get(id=1)):
        #print(description)
        return Transaction.objects.create(user=user, date=date, description=description, amount=amount, category=category)

    def test_transaction_creation(self):
        t = self.create_transaction()
        self.assertTrue(isinstance(t, Transaction))
        #print(t.__str__)
        self.assertEqual(t.__str__(), t.description)


from beans.models import Vendor
class VendorTest(TestCase):

    def create_vendor(self, name="test vendor name", description="test vendor description"):
        return Vendor.objects.create(name=name, description=description)

    def test_vendor_creation(self):
        v = self.create_vendor()
        self.assertTrue(isinstance(v, Vendor))
        self.assertEqual(v.__str__(), v.name)

