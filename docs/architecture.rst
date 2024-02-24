:Django: at least 1.10
:Python: at least 3
:Packages: 
    ``django-allauth`` to authenticate using external providers
    ``whitenoise`` to deploy to Heroku
    ``psycopg2`` to deploy to Heroku
:Documentation: reStructuredText (RST)
:Version control: Git


Attributes
==========

- External authentication. No need to create local users. 
- First time a user is authenticated, its username is recored in the site.
- This site does not store passwords. Every authentication is done against an external provider. 
- Each user can have its own budgets. 
- Each user can have its own transactions. 
- The site allows to upload files with transactions and automatically populate the transactions table for that user. 
- Transactions can be categorized automatically. Categorize means associate a transaction with a category.
- The site produces reports tracking expenditure vs. budget for a given month or year. 


Knobs
=====
Datepicker. http://stackoverflow.com/questions/24245394/django-dateinput-widget-appears-in-chrome-but-not-firefox-or-ie
Make DateInput and DateTimeInput render as a html5 field type="date" and type="datetime"
https://code.djangoproject.com/ticket/21470


An alternative way of populating the form with a particular list
# in the view
@login_required
def budget_new(request):
    '''
    What: Creates a new Budget object.
    How: By using a ModelForm. The first time this view is requested (an HTTP
    GET verb/method) the form is rendered empty. Once the form is filled, this
    same view is requested (but in this second occassion with an HTTP POST
    verb/method) and the data of the filled form is available in the HTML tags.
    '''
    if request.method == "POST":
        form = BudgetForm(request.POST, request=request)
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
            form = BudgetForm(request=request)

    context = {
        'content_header': 'New budget',
        'form': form
    }
    return render(request, 'beans/budget_edit.html', context)

# in the form
class BudgetFormBak(forms.ModelForm):

    class Meta:
        model = Budget
        '''
        note that the Budget model also has an user field,
        but that the form does not show that field
        '''
        fields = ('amount', 'category',)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(BudgetForm, self).__init__(*args, **kwargs)
        '''
        # Original. Delete once confortable the code below is ok
        self.fields["category"].queryset = Category.objects.filter(
            user=self.request.user
        ).order_by(Lower('name'))
        '''
        '''
        Only display in in dropdown those categories for which this user
        does not already have a Budget.
        '''
        '''
        List all the category ids for which a given user as as budget.
        Note this a list of ids. Something of the form
        <QuerySet [10, 14, 23, 6]>
        '''
        categories_budgeted = Budget.objects.filter(
            user=self.request.user
        ).values_list('category', flat=True)

        '''
        Category objects for a given user for which there is not a Budget.
        '''
        categoriess_non_budgeted = Category.objects.filter(
            user=self.request.user
        ).exclude(id__in=categories_budgeted)

        '''
        This is what we render in the drop down: Ordered Category objects for
        a given user for which there is not an existing Budget.
        '''
        self.fields["category"].queryset = categoriess_non_budgeted.order_by(Lower('name'))


