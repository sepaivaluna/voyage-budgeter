from django.contrib import admin
from main_app.models import Budget, Expenditure

# Register your models here.

admin.site.register(Budget)
admin.site.register(Expenditure)