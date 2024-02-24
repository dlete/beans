from django import forms
from django.db.models.functions import Lower
from django.forms.extras.widgets import SelectDateWidget

from .models import Budget, Category, CategoryRule, Document, Transaction

'''
How to use the request (request.user) in a ModelForm in Django
http://stackoverflow.com/questions/8841502/how-to-use-the-request-in-a-modelform-in-django
http://mikethecoder.tumblr.com/post/5865162520/django-form-request-user
http://stackoverflow.com/questions/3010489/how-do-i-filter-values-in-a-django-form-using-modelform
Google search
https://www.google.ie/webhp?sourceid=chrome-instant&ion=1&espv=2&ie=UTF-8#q=request.user%20in%20django%20form
Investigate this:
http://stackoverflow.com/questions/40543272/django-queryset-in-modelform

populate dropdown of form (generic form, not ModelForm)
http://stackoverflow.com/questions/32383978/no-such-column-error-in-django-models

populate dropdown on form (in ModelForm)
http://stackoverflow.com/questions/21719474/django-createview-modelform-dropdown-field-queryset-filter

DateField not showing input type as date
http://stackoverflow.com/questions/22846048/django-form-as-p-datefield-not-showing-input-type-as-date

so that date is rendered as a datepicker
http://stackoverflow.com/questions/22846048/django-form-as-p-datefield-not-showing-input-type-as-date
'''

class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        '''
        note that the Budget model also has an user field,
        but that the form does not show that field
        '''
        fields = ('amount', 'category',)


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        '''
        note that the Category model also has an user field,
        but that the form does not show that field
        '''
        fields = ('name', )


class CategoryRuleForm(forms.ModelForm):
    class Meta:
        model = CategoryRule
        fields = ('category', 'keyword',)
    
    '''
    In this form we sent the full "request" object from the view to this form
    and on initialization we construct the filtered list of objects to render.
    It is simply another way of operating with the form.
    '''
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(CategoryRuleForm, self).__init__(*args, **kwargs)
        
        '''
        Populate the 'category' field with the list of all Categories owned by
        the user in the session. 
        '''
        self.fields["category"].queryset = Category.objects.filter(
            user=self.request.user
        ).order_by(
            Lower('name')
        )


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        '''
        note that the Document model also has an user field,
        but that the form does not show that field
        '''
        fields = ('description', 'document', )


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        '''
        note that the Document model also has an user field,
        but that the form does not show that field
        '''
        fields = ('date', 'description', 'amount', 'category',)

    '''
    In this form we sent the full "request" object from the view to this form
    and on initialization we construct the filtered list of objects to render.
    It is simply another way of operating with the form.
    '''
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(TransactionForm, self).__init__(*args, **kwargs)

        '''
        Populate the 'category' field with the list of all Categories owned by
        the user in the session.
        '''
        self.fields["category"].queryset = Category.objects.filter(
            user=self.request.user
        ).order_by(Lower('name'))


class TransactionEditManyForm(forms.Form):
    #date = forms.DateField(required=False, widget=SelectDateWidget())
    date = forms.DateField(required=False)
    description = forms.CharField(label='Description', max_length=100, required=False)
    amount = forms.DecimalField(label='Amount', required=False)
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False)
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        # if kwargs has no key 'user', user is assigned None
        # make sure your code handles this case gracefully
        super(TransactionEditManyForm, self).__init__(*args, **kwargs)

        self.fields["category"].queryset = Category.objects.filter(
            user=self.user
        ).order_by(Lower('name'))

