from django.conf.urls import url

from . import views

app_name = 'beans'
urlpatterns = [
    url(r'^$', views.transaction_list, name='transaction_list'),
    # should it be about/$ ?????
    url(r'^about$', views.about, name='about'),
    url(r'^faq$', views.faq, name='faq'),
    url(r'^budget_new$', views.budget_new, name='budget_new'),
    url(r'^budget_list$', views.budget_list, name='budget_list'),
    url(r'^budget/(?P<pk>\d+)/$', views.budget_detail, name='budget_detail'),
    url(r'^budget/(?P<pk>\d+)/delete/$', views.budget_delete, name='budget_delete'),
    url(r'^budget/(?P<pk>\d+)/edit/$', views.budget_edit, name='budget_edit'),
    url(r'^category_new$', views.category_new, name='category_new'),
    url(r'^category_list$', views.category_list, name='category_list'),
    url(r'^category/(?P<pk>\d+)/$', views.category_detail, name='category_detail'),
    url(r'^category/(?P<pk>\d+)/delete/$', views.category_delete, name='category_delete'),
    url(r'^category/(?P<pk>\d+)/edit/$', views.category_edit, name='category_edit'),
    url(r'^category_rule_new$', views.category_rule_new, name='category_rule_new'),
    url(r'^category_rule_list$', views.category_rule_list, name='category_rule_list'),
    url(r'^category_rule/(?P<pk>\d+)/$', views.category_rule_detail, name='category_rule_detail'),
    url(r'^category_rule/(?P<pk>\d+)/delete/$', views.category_rule_delete, name='category_rule_delete'),
    url(r'^category_rule/(?P<pk>\d+)/edit/$', views.category_rule_edit, name='category_rule_edit'),
    url(r'^document/(?P<pk>\d+)/delete/$', views.document_delete, name='document_delete'),
    url(r'^document_import/(?P<document_id>[0-9]+)/$', views.document_import, name='document_import'),
    url(r'^document_new$', views.document_new, name='document_new'),
    url(r'^document_list$', views.document_list, name='document_list'),
    url(r'^report_month$', views.report_month, name='report_month'),
    url(r'^report_year$', views.report_year, name='report_year'),
    url(r'^set_user_initial_data$', views.set_user_initial_data, name='set_user_initial_data'),
    url(r'^transaction_new$', views.transaction_new, name='transaction_new'),
    url(r'^transaction_list$', views.transaction_list, name='transaction_list'),
    url(r'^transaction/(?P<pk>\d+)/$', views.transaction_detail, name='transaction_detail'),
    url(r'^transaction/(?P<pk>\d+)/auto_classify/$', views.transaction_auto_classify, name='transaction_auto_classify'),
    url(r'^transaction/(?P<pk>\d+)/delete/$', views.transaction_delete, name='transaction_delete'),
    url(r'^transaction/(?P<pk>\d+)/edit/$', views.transaction_edit, name='transaction_edit'),
    url(r'^transaction_edit_many/$', views.transaction_edit_many, name='transaction_edit_many'),
    url(r'^transaction_update_many/$', views.transaction_update_many, name='transaction_update_many'),
]
