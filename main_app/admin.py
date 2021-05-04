from django.contrib import admin
from main_app.models import Budget, City, Expenditure, PurchasePhotos

# Register your models here.

admin.site.register(Budget)
admin.site.register(Expenditure)
admin.site.register(PurchasePhotos)
admin.site.register(City)