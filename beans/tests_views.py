from django.test import TestCase

# Create your tests here.
#https://realpython.com/blog/python/testing-in-django-part-1-best-practices-and-examples/

# models test
#from django.contrib.auth.models import *
#from beans.models import Budget
#from beans.models import Category


''' view tests, begin '''
from django.test import Client

class AboutTest(TestCase):
    def setUp(self):
        # Every test needs a client.
        self.client = Client()

    def test_about(self):
        # Issue a GET request.
        response = self.client.get('/beans/about')

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        # Check that the body contanins this text
        self.assertContains(response, "First step")
        self.assertContains(response, "Create Budgets")
        self.assertContains(response, "Second step")
        self.assertContains(response, "Enter Transactions")
        self.assertContains(response, "Third step")
        self.assertContains(response, "Track Expenditure vs. Budget with th")



from django.contrib.auth import get_user_model

class BudgetTest(TestCase):
    '''
    so that I can bypass unittest not being able to check external sites, and
    hence not being able to test django_allauth
    http://stackoverflow.com/questions/27841101/can-not-log-in-with-unit-test-in-django-allauth
    '''
    def setUp(self):
        # Every test needs a client.
        self.client = Client()
        username = 'testuser'
        password = 'testpass'
        User = get_user_model()
        user = User.objects.create_user(username=username, password=password)
        logged_in = self.client.login(username=username, password=password)
        self.assertTrue(logged_in)

    def test_budget_new(self):
        # Issue a GET request.
        response = self.client.get('/beans/budget_new')

        # Check that the response is 200 OK.
        # should not be redirected to external authenticators since the user
        # is already logged as part of the SetUp
        self.assertEqual(response.status_code, 200)
''' view tests, end '''
