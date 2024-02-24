from django.db import models
from django.conf import settings

''' 
If you need reference for Model Meta Options
https://docs.djangoproject.com/en/1.10/ref/models/options/

The order of the Models in this file is important. For a ForeignKey to be 
reference, the Model where that ForeignKey is defined must appear first in
the file. For example: the Budget model must appear, in this file, after the 
Category model; reason being that Budget does use Category as ForeignKey. 

ForeignKey to User is with settings.AUTH_USER_MODEL, not with 'auth.User'
https://docs.djangoproject.com/en/1.10/topics/auth/customizing/#reusable-apps-and-auth-user-model

This problem did arise during a migration. Appears to be that it was querying 
the database while models are still loading and apps are not fully initialized.
django.db.utils.OperationalError: no such column: 
http://stackoverflow.com/questions/32383978/no-such-column-error-in-django-models
'''

class Category(models.Model):
    '''
    This model is a list of categories. Categories are not user specific, the
    same categories are shown to all the users.
    '''
    name = models.CharField(
        blank=False, 
        max_length=200, 
        null=False,
        #unique=True, 
        verbose_name='Category name',
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE
    )
    class Meta:
        ordering            = ['name']
        unique_together     = (("name", "user"),)
        verbose_name        = 'Expense categories'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Budget(models.Model):
    '''
    This model associates a budget to each category. That budget is also unique
    for each user. A given user can have one and only one budget for each 
    category
    '''
    amount = models.DecimalField(
        blank=False, 
        decimal_places=2, 
        max_digits=10,
    )
    category = models.ForeignKey(
        Category, 
        blank=False, 
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=False,
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering        = ['category']
        unique_together = (("user", "category"),)

    def __str__(self):
        return self.category.name


class CategoryRule(models.Model):
    '''
    This model serves as auxialiary help for the clasification of transactions
    into a given Category. This model provides a series of relations:
    "keyword" vs "category"
    so that if the keyword is in a string, then that string can be associated 
    with that Category.
    '''
    category = models.ForeignKey(
        Category, 
        blank=False,
        on_delete=models.CASCADE,
    )
    keyword = models.CharField(
        blank=False, 
        max_length=50,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=False,
        on_delete=models.CASCADE,
    )

    class Meta:
        # keywords and categories can be repeated, but NOT for a given user.
        unique_together = (("category", "keyword", "user"),)

    def __str__(self):
        return self.keyword



class Document(models.Model):
    '''
    This model records the location of uploaded files.
    '''
    description = models.CharField(
        blank=True, 
        max_length=255,
    )
    document = models.FileField(
        blank=False, 
        upload_to='documents/',
    )
    uploaded_at = models.DateTimeField(
        auto_now_add=True,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=False,
        on_delete=models.CASCADE,
    )


class Transaction(models.Model):
    '''
    This model records transactions, storing for each record and amount (no
    currency associated to it at the moment, just a generic numeric figure), a
    date, category and user. 
    '''
    amount = models.DecimalField(
        help_text="A number/figure, please use the format: <em>dd.cc</em>", 
        max_digits=10, 
        decimal_places=2,
    )
    category = models.ForeignKey(
        Category,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    date = models.DateField('transaction date')
    description = models.CharField(
        blank=False, 
        max_length=200,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering            = ['date']
        ordering            = ['category']
        '''
        So that these fields cannot be all together the same at any given time.
        '''
        #unique_together = (("amount", "date", "description", "user"),)

    def __str__(self):
        return self.description



class Vendor(models.Model):
    '''
    In this model, records of Vendors/Companies, storing a name a description.
    '''
    name = models.CharField(
        max_length=200, 
        unique=True, 
        verbose_name='Vendor name',
    )
    description = models.CharField(
        blank=True,
        max_length=200,
    )

    class Meta:
        ordering            = ['name']
        verbose_name        = 'Vendor or Merchant'
        verbose_name_plural = 'Vendors/Merchants'

    def __str__(self):
        return self.name

