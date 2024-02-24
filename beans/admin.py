from django.contrib import admin

# Register your models here.
from .models import Budget, Category, CategoryRule, Document, Transaction, Vendor

class BudgetAdmin(admin.ModelAdmin):
    list_display = ('user', 'category', 'amount')
    list_filter = ('user', 'category')
    ordering = ('user', 'category')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'name')
    list_filter = ('user', 'name')
    ordering = ('user', 'name')

class CategoryRuleAdmin(admin.ModelAdmin):
    list_display = ('user', 'keyword', 'category')
    list_filter = ('user', 'category')
    ordering = ('user', 'category')

class DocumentAdmin(admin.ModelAdmin):
    list_display = ('user', 'document')
    list_filter = ('user', 'document')
    ordering = ('user', 'document')

class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'description', 'amount', 'category')
    list_filter = ('user', 'date', 'category')
    ordering = ('user', '-date', 'category')

class VendorAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

admin.site.register(Budget, BudgetAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(CategoryRule, CategoryRuleAdmin)
admin.site.register(Document, DocumentAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Vendor, VendorAdmin)

